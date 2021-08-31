from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


def load_path_video(instance, filename):
    return '/'.join(['video', str(instance.title) + str(".mp4")])


def load_path_thum(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['thum', str(instance.title) + str(".") + str(ext)])


class UserManager(BaseUserManager):
    # email認証のためのオーバーライド
    def create_user(self, email, password=None, **extra_fields):
        # emailがない時
        if not email:
            raise ValueError('Email address is must')

        # normalize_emailは入力されたメールアドレスを正規化する
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # DBに保存
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # ユニバーサルユニークIDとプライマリーキーの使用と、編集不可
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    # 最大文字数255文字、ユニーク必須
    email = models.EmailField(max_length=255, unique=True)
    # 最大文字数255文字、空白OK
    username = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    # スタッフ権限はなし
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


# 動画の内容を扱うモデル
class Video(models.Model):
    # ビデオのID
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    # タイトルとvideoとサムネイルは必須
    title = models.CharField(max_length=30, blank=False)
    video = models.FileField(blank=False, upload_to=load_path_video)
    thum = models.ImageField(blank=False, upload_to=load_path_thum)
    # 高評価
    like = models.IntegerField(default=0)
    # 低評価
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return self.title
