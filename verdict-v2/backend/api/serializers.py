from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .models import (VictimFile, FileReview, GameProgress, LeaderboardEntry,
                     InterrogationSession, InterrogationMessage, AnonymousTip,
                     CorruptionEvent, PlayerCorruptionResolved, TimelineEvent)

Player = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model  = Player
        fields = ['id','first_name','last_name','username','email','age','sex','phone_number','password','confirm_password']

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        player   = Player(**validated_data)
        player.set_password(password)
        player.save()
        GameProgress.objects.create(player=player)
        return player


class PlayerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Player
        fields = ['id','first_name','last_name','username','email','age','sex','phone_number',
                  'terms_accepted','cinematic_viewed','created_at']
        read_only_fields = ['id','created_at','terms_accepted','cinematic_viewed']


class AcceptTermsSerializer(serializers.Serializer):
    accepted = serializers.BooleanField()
    def validate_accepted(self, v):
        if not v: raise serializers.ValidationError("You must accept the Terms.")
        return v


class VictimFileSerializer(serializers.ModelSerializer):
    is_reviewed  = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    is_unlocked  = serializers.SerializerMethodField()

    class Meta:
        model  = VictimFile
        fields = ['id','file_id','code_name','victim_age','incident_year','location',
                  'status','status_label','evidence_strength','evidence_items',
                  'unlock_tier','has_cipher','is_corrupted','corruption_blocker',
                  'is_reviewed','is_unlocked']

    def get_is_reviewed(self, obj):
        req = self.context.get('request')
        if req and req.user.is_authenticated:
            return FileReview.objects.filter(player=req.user, victim_file=obj).exists()
        return False

    def get_status_label(self, obj):
        return obj.get_status_display()

    def get_is_unlocked(self, obj):
        req = self.context.get('request')
        if not req or not req.user.is_authenticated:
            return obj.unlock_tier == '1'
        try:
            reviewed = req.user.progress.files_reviewed
        except Exception:
            reviewed = 0
        tier_map = {'1': 0, '2': 2, '3': 4, '4': 6}
        return reviewed >= tier_map.get(obj.unlock_tier, 0)


class FileReviewSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(source='victim_file.file_id', read_only=True)
    class Meta:
        model  = FileReview
        fields = ['id','file_id','reviewed_at','notes','cipher_solved']
        read_only_fields = ['reviewed_at']


class GameProgressSerializer(serializers.ModelSerializer):
    total_files  = serializers.SerializerMethodField()
    player_name  = serializers.SerializerMethodField()
    class Meta:
        model  = GameProgress
        fields = ['files_reviewed','total_files','conviction_strength','verdict_reached',
                  'verdict_reached_at','time_remaining_secs','tips_read','ciphers_solved',
                  'corruption_overcome','score','session_start','player_name']

    def get_total_files(self, obj):
        return VictimFile.objects.count()

    def get_player_name(self, obj):
        p = obj.player
        return f"{p.first_name} {p.last_name}".strip() or p.username


class LeaderboardSerializer(serializers.ModelSerializer):
    username     = serializers.CharField(source='player.username')
    display_name = serializers.SerializerMethodField()
    class Meta:
        model  = LeaderboardEntry
        fields = ['rank','username','display_name','score','conviction_pct','completion_time','verdict_reached']

    def get_display_name(self, obj):
        p = obj.player
        return f"{p.first_name} {p.last_name}".strip() or p.username


class InterrogationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InterrogationMessage
        fields = ['id','role','content','created_at']


class InterrogationSessionSerializer(serializers.ModelSerializer):
    messages = InterrogationMessageSerializer(many=True, read_only=True)
    class Meta:
        model  = InterrogationSession
        fields = ['id','suspect','started_at','is_active','clue_unlocked','messages']


class AnonymousTipSerializer(serializers.ModelSerializer):
    category_label = serializers.SerializerMethodField()
    class Meta:
        model  = AnonymousTip
        fields = ['id','title','content','category','category_label','sender_alias','unlock_after_reviews']

    def get_category_label(self, obj):
        return obj.get_category_display()


class CorruptionEventSerializer(serializers.ModelSerializer):
    severity_label = serializers.SerializerMethodField()
    is_resolved    = serializers.SerializerMethodField()
    class Meta:
        model  = CorruptionEvent
        fields = ['id','title','description','severity','severity_label','blocker_name',
                  'blocker_role','resolution','is_resolved']

    def get_severity_label(self, obj):
        return obj.get_severity_display()

    def get_is_resolved(self, obj):
        req = self.context.get('request')
        if req and req.user.is_authenticated:
            return PlayerCorruptionResolved.objects.filter(player=req.user, event=obj).exists()
        return False


class TimelineEventSerializer(serializers.ModelSerializer):
    category_label = serializers.SerializerMethodField()
    class Meta:
        model  = TimelineEvent
        fields = ['id','year','month','title','description','category','category_label','is_locked','unlock_after_reviews']

    def get_category_label(self, obj):
        return obj.get_category_display()
