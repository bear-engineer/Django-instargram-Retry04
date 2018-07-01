from django.contrib.auth.models import AbstractUser
from django.db import models
from members.exceptions import RelationNotExist, DuplicateRelationException

class User(AbstractUser):
    profile_image = models.ImageField(blank=True, upload_to='profile')
    site = models.URLField(blank=True)
    email = models.EmailField()
    CHOICE_GENDER = (
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택하지 않습니다.')
    )
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER)
    created_at = models.DateTimeField(auto_now_add=True)
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.username

    def follow(self, to_user):
        if self.relations_by_from_user.filter(to_user=to_user).exists():
            raise DuplicateRelationException(
                from_user=self,
                to_user=to_user,
                relation_type='follow'
            )

        return self.relations_by_from_user.create(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    def unfollow(self, to_user):
        # 아래 경우가 존재하면 실행
        # 존재하지 않으면 Exception
        q = self.relations_by_from_user.filter(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )
        if q:
            q.delete()
        else:
            raise RelationNotExist(
                from_user=self,
                to_user=to_user,
                relation_type='Follow',
            )

    @property
    def following(self):
        # 내가 follow중인 User QuerySet리턴
        return User.objects.filter(
            relations_by_to_user__form_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
            )

    @property
    def followers(self):
        # 나를 follow중인 User QuerySet
        # return User.objects.filter(pk__in=self.follower_relations.values('from_user'))
        return User.objects.filter(
            relations_by_to_from__to_user=self,
            relations_by_to_from__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def block_users(self):
        # 내가 block중인 User QuerySet
        # return User.objects.filter(pk__in=self.block_relations.values('to_user'))
        return User.objects.filter(
            relations_by_to_to__from_user=self,
            relations_by_to_to__relation_type=Relation.RELATION_TYPE_BLOCK,
        )

    @property
    def following_relations(self):
        # 내가 follow중인 Relation Query리턴
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def follower_relations(self):
        # 나를 follow중인 Relation Query리턴
        return self.relations_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def block_relations(self):
        # 내가 block한 Relation Query리턴
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_BLOCK,
        )


class Relation(models.Model):
    RELATION_TYPE_BLOCK = 'b'
    RELATION_TYPE_FOLLOW = 'f'

    CHOICES_RELATION_TYPE = (
        (RELATION_TYPE_FOLLOW, 'Follow'),
        (RELATION_TYPE_BLOCK, 'Block')
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_from_user',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_to_user',
    )

    relation_type = models.CharField(max_length=1, choices=CHOICES_RELATION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'From {from_user} to {to_user} ({type})'.format(
            from_user=self.from_user.username,
            to_user=self.to_user.username,
            type=self.get_relation_type_display(),
        )
