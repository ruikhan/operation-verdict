from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random, string


class Player(AbstractUser):
    SEX_CHOICES = [('M','Male'),('F','Female'),('O','Other'),('N','Prefer not to say')]
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    terms_accepted = models.BooleanField(default=False)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    cinematic_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class VictimFile(models.Model):
    STATUS_CHOICES = [
        ('pending','Testimony Pending'), ('corroborated','Corroborated'),
        ('sealed','Sealed — Classified'), ('active','Witness Cooperation Active'),
        ('cold','Cold — Needs Review'), ('original','Original Complaint Filed'),
        ('recanted','Testimony Recanted'), ('high_confidence','High Confidence'),
    ]
    TIER_CHOICES = [('1','Tier 1 — Unlocked'),('2','Tier 2 — Requires 2 reviews'),
                    ('3','Tier 3 — Requires 4 reviews'),('4','Tier 4 — Requires 6 reviews')]

    file_id           = models.CharField(max_length=10, unique=True)
    code_name         = models.CharField(max_length=60)
    victim_age        = models.PositiveSmallIntegerField()
    incident_year     = models.PositiveSmallIntegerField()
    location          = models.CharField(max_length=120)
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES)
    evidence_strength = models.PositiveSmallIntegerField(help_text="0–100")
    evidence_items    = models.JSONField(default=list)
    unlock_tier       = models.CharField(max_length=1, choices=TIER_CHOICES, default='1')
    has_cipher        = models.BooleanField(default=False)
    cipher_key        = models.CharField(max_length=200, blank=True)
    cipher_solution   = models.CharField(max_length=200, blank=True)
    is_corrupted      = models.BooleanField(default=False)
    corruption_blocker= models.CharField(max_length=100, blank=True)
    reviewed_by       = models.ManyToManyField('Player', through='FileReview', blank=True, related_name='reviewed_files')

    class Meta:
        ordering = ['unlock_tier', 'file_id']

    def __str__(self):
        return f"{self.file_id} — {self.code_name}"


class FileReview(models.Model):
    player      = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reviews')
    victim_file = models.ForeignKey(VictimFile, on_delete=models.CASCADE, related_name='reviews')
    reviewed_at = models.DateTimeField(auto_now_add=True)
    notes       = models.TextField(blank=True)
    cipher_solved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('player', 'victim_file')
        ordering = ['-reviewed_at']


class GameProgress(models.Model):
    player               = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='progress')
    files_reviewed       = models.PositiveSmallIntegerField(default=0)
    conviction_strength  = models.FloatField(default=0.0)
    verdict_reached      = models.BooleanField(default=False)
    verdict_reached_at   = models.DateTimeField(null=True, blank=True)
    session_start        = models.DateTimeField(null=True, blank=True)
    session_end          = models.DateTimeField(null=True, blank=True)
    time_remaining_secs  = models.IntegerField(default=7200)  # 2 hour timer
    tips_read            = models.PositiveSmallIntegerField(default=0)
    ciphers_solved       = models.PositiveSmallIntegerField(default=0)
    corruption_overcome  = models.PositiveSmallIntegerField(default=0)
    score                = models.IntegerField(default=0)
    last_active          = models.DateTimeField(auto_now=True)

    def recalculate_score(self):
        base = self.conviction_strength * 10
        time_bonus = max(0, self.time_remaining_secs // 60) * 5
        cipher_bonus = self.ciphers_solved * 200
        tip_bonus = self.tips_read * 50
        corruption_bonus = self.corruption_overcome * 150
        self.score = int(base + time_bonus + cipher_bonus + tip_bonus + corruption_bonus)

    def __str__(self):
        return f"{self.player.username} — {self.conviction_strength:.1f}%"


class LeaderboardEntry(models.Model):
    player           = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='leaderboard')
    score            = models.IntegerField(default=0)
    conviction_pct   = models.FloatField(default=0.0)
    completion_time  = models.IntegerField(default=0, help_text="seconds taken")
    verdict_reached  = models.BooleanField(default=False)
    rank             = models.IntegerField(default=0)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', 'completion_time']

    def __str__(self):
        return f"#{self.rank} {self.player.username} — {self.score}pts"


class InterrogationSession(models.Model):
    player     = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='interrogations')
    suspect    = models.CharField(max_length=100, default='Jipri Eipstein')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at   = models.DateTimeField(null=True, blank=True)
    is_active  = models.BooleanField(default=True)
    clue_unlocked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.player.username} interrogates {self.suspect}"


class InterrogationMessage(models.Model):
    ROLE_CHOICES = [('investigator','Investigator'),('suspect','Suspect')]
    session    = models.ForeignKey(InterrogationSession, on_delete=models.CASCADE, related_name='messages')
    role       = models.CharField(max_length=15, choices=ROLE_CHOICES)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class AnonymousTip(models.Model):
    CATEGORY_CHOICES = [
        ('location','Location Intel'),('associate','Associate Info'),
        ('financial','Financial Trail'),('witness','Witness Info'),
        ('evidence','Evidence Pointer'),
    ]
    title       = models.CharField(max_length=120)
    content     = models.TextField()
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sender_alias= models.CharField(max_length=60, default='Anonymous')
    unlock_after_reviews = models.PositiveSmallIntegerField(default=0)
    linked_file = models.ForeignKey(VictimFile, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='tips')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['unlock_after_reviews', 'created_at']

    def __str__(self):
        return f"[{self.category}] {self.title}"


class PlayerTipRead(models.Model):
    player  = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tips_read_set')
    tip     = models.ForeignKey(AnonymousTip, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'tip')


class CorruptionEvent(models.Model):
    SEVERITY_CHOICES = [('low','Low — Minor Delay'),('medium','Medium — Evidence Suppressed'),
                        ('high','High — File Blocked')]
    title       = models.CharField(max_length=120)
    description = models.TextField()
    severity    = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    blocker_name= models.CharField(max_length=100)
    blocker_role= models.CharField(max_length=100)
    resolution  = models.TextField(help_text="What player must do to overcome this")
    resolution_code = models.CharField(max_length=50, help_text="Secret code to unlock")
    affected_file = models.ForeignKey(VictimFile, null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name='corruption_events')
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.severity}] {self.title}"


class PlayerCorruptionResolved(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='resolved_corruptions')
    event  = models.ForeignKey(CorruptionEvent, on_delete=models.CASCADE)
    resolved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'event')


class TimelineEvent(models.Model):
    CATEGORY_CHOICES = [('ascent','Rise to Power'),('crime','Criminal Act'),
                        ('cover_up','Cover-Up'),('exposure','Exposure'),('legal','Legal Action')]
    year        = models.IntegerField()
    month       = models.IntegerField(null=True, blank=True)
    title       = models.CharField(max_length=150)
    description = models.TextField()
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_locked   = models.BooleanField(default=False)
    unlock_after_reviews = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['year', 'month']

    def __str__(self):
        return f"{self.year} — {self.title}"
