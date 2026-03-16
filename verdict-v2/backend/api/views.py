import os
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (VictimFile, FileReview, GameProgress, LeaderboardEntry,
                     InterrogationSession, InterrogationMessage, AnonymousTip,
                     PlayerTipRead, CorruptionEvent, PlayerCorruptionResolved, TimelineEvent)
from .serializers import (RegisterSerializer, PlayerProfileSerializer, AcceptTermsSerializer,
                           VictimFileSerializer, FileReviewSerializer, GameProgressSerializer,
                           LeaderboardSerializer, InterrogationSessionSerializer,
                           AnonymousTipSerializer, CorruptionEventSerializer, TimelineEventSerializer)

Player = get_user_model()


# ── Auth ──────────────────────────────────────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        self.perform_create(s)
        return Response({'detail': 'Investigator profile created.'}, status=status.HTTP_201_CREATED)


# ── Player ────────────────────────────────────────────────────────────────────
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PlayerProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self): return self.request.user


class AcceptTermsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        s = AcceptTermsSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = request.user
        if not user.terms_accepted:
            user.terms_accepted = True
            user.terms_accepted_at = timezone.now()
            user.save(update_fields=['terms_accepted', 'terms_accepted_at'])
        return Response({'detail': 'Terms accepted.', 'terms_accepted': True})


class CinematicCompleteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if not user.cinematic_viewed:
            user.cinematic_viewed = True
            user.save(update_fields=['cinematic_viewed'])
        # Start game timer
        prog, _ = GameProgress.objects.get_or_create(player=user)
        if not prog.session_start:
            prog.session_start = timezone.now()
            prog.save(update_fields=['session_start'])
        return Response({'detail': 'Briefing acknowledged.'})


# ── Game — Files ───────────────────────────────────────────────────────────────
class VictimFileListView(generics.ListAPIView):
    serializer_class = VictimFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            reviewed = self.request.user.progress.files_reviewed
        except Exception:
            reviewed = 0
        tier_map = {'1': 0, '2': 2, '3': 4, '4': 6}
        available = [f for f in VictimFile.objects.all()
                     if reviewed >= tier_map.get(f.unlock_tier, 0)]
        return available

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class VictimFileDetailView(generics.RetrieveAPIView):
    queryset = VictimFile.objects.all()
    serializer_class = VictimFileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'file_id'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class ReviewFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, file_id):
        try:
            vf = VictimFile.objects.get(file_id=file_id)
        except VictimFile.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=404)

        review, created = FileReview.objects.get_or_create(
            player=request.user, victim_file=vf,
            defaults={'notes': request.data.get('notes', '')}
        )

        if created:
            prog, _ = GameProgress.objects.get_or_create(player=request.user)
            reviewed_qs = VictimFile.objects.filter(reviews__player=request.user)
            prog.files_reviewed = reviewed_qs.count()
            if reviewed_qs.exists():
                avg = sum(f.evidence_strength for f in reviewed_qs) / reviewed_qs.count()
                ratio = prog.files_reviewed / VictimFile.objects.count()
                prog.conviction_strength = (avg * 0.75) + (ratio * 100 * 0.25)
            if prog.files_reviewed >= VictimFile.objects.count() and not prog.verdict_reached:
                prog.verdict_reached = True
                prog.verdict_reached_at = timezone.now()
            prog.recalculate_score()
            prog.save()

            # Update leaderboard
            lb, _ = LeaderboardEntry.objects.get_or_create(player=request.user)
            lb.score = prog.score
            lb.conviction_pct = prog.conviction_strength
            lb.verdict_reached = prog.verdict_reached
            if prog.verdict_reached and prog.session_start:
                lb.completion_time = int((timezone.now() - prog.session_start).total_seconds())
            lb.save()
            _rerank_leaderboard()

        return Response({
            'created': created,
            'review': FileReviewSerializer(review).data,
            'progress': GameProgressSerializer(request.user.progress).data,
        })


class SolveCipherView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, file_id):
        try:
            vf = VictimFile.objects.get(file_id=file_id)
        except VictimFile.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=404)

        if not vf.has_cipher:
            return Response({'detail': 'No cipher for this file.'}, status=400)

        answer = request.data.get('answer', '').strip().upper()
        correct = vf.cipher_solution.strip().upper()

        if answer == correct:
            FileReview.objects.filter(player=request.user, victim_file=vf).update(cipher_solved=True)
            prog, _ = GameProgress.objects.get_or_create(player=request.user)
            prog.ciphers_solved += 1
            prog.recalculate_score()
            prog.save()
            return Response({'correct': True, 'detail': 'Cipher solved! Evidence unlocked.'})
        return Response({'correct': False, 'detail': 'Incorrect. Try again.'})


# ── Timer ──────────────────────────────────────────────────────────────────────
class UpdateTimerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seconds = request.data.get('time_remaining_secs')
        if seconds is None:
            return Response({'detail': 'time_remaining_secs required.'}, status=400)
        prog, _ = GameProgress.objects.get_or_create(player=request.user)
        prog.time_remaining_secs = max(0, int(seconds))
        if prog.time_remaining_secs == 0 and not prog.session_end:
            prog.session_end = timezone.now()
        prog.recalculate_score()
        prog.save()
        return Response({'time_remaining_secs': prog.time_remaining_secs})


# ── Leaderboard ────────────────────────────────────────────────────────────────
class LeaderboardView(generics.ListAPIView):
    queryset = LeaderboardEntry.objects.all()[:20]
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]


# ── Interrogation ──────────────────────────────────────────────────────────────
class StartInterrogationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        InterrogationSession.objects.filter(player=request.user, is_active=True).update(is_active=False)
        session = InterrogationSession.objects.create(
            player=request.user,
            suspect=request.data.get('suspect', 'Jipri Eipstein')
        )
        return Response({'session_id': session.id, 'suspect': session.suspect})


class SendInterrogationMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = InterrogationSession.objects.get(id=session_id, player=request.user)
        except InterrogationSession.DoesNotExist:
            return Response({'detail': 'Session not found.'}, status=404)

        question = request.data.get('message', '').strip()
        if not question:
            return Response({'detail': 'Message required.'}, status=400)

        InterrogationMessage.objects.create(session=session, role='investigator', content=question)

        history = list(session.messages.all())
        messages_for_api = [
            {'role': 'user' if m.role == 'investigator' else 'assistant', 'content': m.content}
            for m in history
        ]

        api_key = os.environ.get('ANTHROPIC_API_KEY', '')

        if api_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                suspect = session.suspect
                system_prompt = f"""You are playing the role of {suspect} being interrogated by an investigator.
You are a wealthy, powerful individual accused of serious crimes involving the trafficking and abuse of young women.
You are evasive, manipulative, and arrogant. You sometimes slip up and reveal hints.
Keep responses to 2-4 sentences. Occasionally drop subtle clues about evidence, locations, or associates.
Never directly confess but let the investigator feel they are making progress.
Reference locations like Palm Beach, Little St. James island, Manhattan, Paris.
Mention associates obliquely. Stay in character at all times."""

                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=300,
                    system=system_prompt,
                    messages=messages_for_api
                )
                reply = response.content[0].text
            except Exception as e:
                reply = _fallback_response(question, session.suspect)
        else:
            reply = _fallback_response(question, session.suspect)

        InterrogationMessage.objects.create(session=session, role='suspect', content=reply)

        # Unlock clue after 5 exchanges
        if session.messages.count() >= 10 and not session.clue_unlocked:
            session.clue_unlocked = True
            session.save(update_fields=['clue_unlocked'])
            prog, _ = GameProgress.objects.get_or_create(player=request.user)
            prog.conviction_strength = min(100, prog.conviction_strength + 5)
            prog.recalculate_score()
            prog.save()

        return Response({
            'reply': reply,
            'clue_unlocked': session.clue_unlocked,
            'session_id': session.id,
        })


def _fallback_response(question, suspect):
    q = question.lower()
    if any(w in q for w in ['island', 'st. james', 'caribbean']):
        return "That island was merely a private retreat for relaxation. Many powerful people enjoyed my hospitality there. I can't help what others did on their own time."
    if any(w in q for w in ['girl', 'victim', 'abuse', 'traffick']):
        return "These are outrageous allegations from individuals seeking financial gain. My lawyers have documentation that completely exonerates me."
    if any(w in q for w in ['money', 'fund', 'financ', 'wire']):
        return "My financial arrangements are entirely legitimate. Complex, yes — but entirely legal. My clients trusted me precisely because I understood discretion."
    if any(w in q for w in ['maxwell', 'ghilaine', 'associate']):
        return "I had many associates in my social circles. I cannot be held responsible for the independent actions of every acquaintance."
    if any(w in q for w in ['palm beach', 'florida', 'mansion']):
        return "Palm Beach was simply one of my residences. I entertained many prominent figures there. That is not a crime, last I checked."
    return "I find this line of questioning quite tedious. My attorneys have advised me not to discuss specifics. What I will say is that everything I did was within the bounds of the law — or at least, within the bounds of what could be proven."


# ── Tips ───────────────────────────────────────────────────────────────────────
class TipListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            reviewed = request.user.progress.files_reviewed
        except Exception:
            reviewed = 0
        tips = AnonymousTip.objects.filter(unlock_after_reviews__lte=reviewed)
        read_ids = set(PlayerTipRead.objects.filter(player=request.user).values_list('tip_id', flat=True))
        data = []
        for tip in tips:
            d = AnonymousTipSerializer(tip).data
            d['is_read'] = tip.id in read_ids
            data.append(d)
        return Response(data)


class ReadTipView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tip_id):
        try:
            tip = AnonymousTip.objects.get(id=tip_id)
        except AnonymousTip.DoesNotExist:
            return Response({'detail': 'Tip not found.'}, status=404)
        _, created = PlayerTipRead.objects.get_or_create(player=request.user, tip=tip)
        if created:
            prog, _ = GameProgress.objects.get_or_create(player=request.user)
            prog.tips_read += 1
            prog.recalculate_score()
            prog.save()
        return Response({'read': True})


# ── Corruption ─────────────────────────────────────────────────────────────────
class CorruptionEventListView(generics.ListAPIView):
    serializer_class = CorruptionEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CorruptionEvent.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class ResolveCorruptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = CorruptionEvent.objects.get(id=event_id)
        except CorruptionEvent.DoesNotExist:
            return Response({'detail': 'Event not found.'}, status=404)

        code = request.data.get('code', '').strip().upper()
        if code != event.resolution_code.upper():
            return Response({'correct': False, 'detail': 'Incorrect access code.'})

        _, created = PlayerCorruptionResolved.objects.get_or_create(player=request.user, event=event)
        if created:
            prog, _ = GameProgress.objects.get_or_create(player=request.user)
            prog.corruption_overcome += 1
            prog.recalculate_score()
            prog.save()

        return Response({'correct': True, 'detail': 'Corruption barrier bypassed.'})


# ── Timeline ───────────────────────────────────────────────────────────────────
class TimelineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            reviewed = request.user.progress.files_reviewed
        except Exception:
            reviewed = 0
        events = TimelineEvent.objects.all()
        data = []
        for ev in events:
            d = TimelineEventSerializer(ev).data
            d['is_unlocked'] = not ev.is_locked or reviewed >= ev.unlock_after_reviews
            data.append(d)
        return Response(data)


# ── Progress ───────────────────────────────────────────────────────────────────
class GameProgressView(generics.RetrieveAPIView):
    serializer_class = GameProgressSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        prog, _ = GameProgress.objects.get_or_create(player=self.request.user)
        return prog


# ── Helpers ────────────────────────────────────────────────────────────────────
def _rerank_leaderboard():
    entries = LeaderboardEntry.objects.order_by('-score', 'completion_time')
    for i, entry in enumerate(entries, 1):
        entry.rank = i
        entry.save(update_fields=['rank'])
