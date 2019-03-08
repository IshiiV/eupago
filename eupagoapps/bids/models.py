from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count, Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from eupagoapps.bids.managers import ProductBidQuerySet
from oscar.core import validators
from oscar.core.compat import AUTH_USER_MODEL


@python_2_unicode_compatible
class ProductBid(models.Model):
    """
    A Bid of a product

    Reviews can belong to a user or be anonymous.
    """

    # Note we keep the bid even if the product is deleted
    product = models.ForeignKey(
        'catalogue.Product', related_name='bids', null=True,
        on_delete=models.SET_NULL)


    # Lances do cliente
    user_bid1 = models.DecimalField(
        _("User bid 1"), decimal_places=2, max_digits=12)
    user_bid2 = models.DecimalField(
        _("User bid 2"), decimal_places=2, max_digits=12, null=True, blank=True)
    user_bid3 = models.DecimalField(
        _("User bid 3"), decimal_places=2, max_digits=12, null=True, blank=True)

   
    # User information.
    user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='bids', null=True, blank=True)

    # Fields to be complete d if user is anonymous
    name = models.CharField(
        pgettext_lazy(u"Anonymous name", u"Name"),
        max_length=255, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    homepage = models.URLField(_("URL"), blank=True)

    FOR_MODERATION, APPROVED, REJECTED = 0, 1, 2
    STATUS_CHOICES = (
        (FOR_MODERATION, _("Requires moderation")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )
    default_status = APPROVED
    #if settings.OSCAR_MODERATE_BIDS:
    #    default_status = FOR_MODERATION
    status = models.SmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=default_status)

    date_created = models.DateTimeField(auto_now_add=True)

    # Managers
    objects = ProductBidQuerySet.as_manager()

    class Meta:
        abstract = False
        app_label = 'bids'
        ordering = ['id']
        unique_together = (('product', 'user'),)
        verbose_name = _('Product bid')
        verbose_name_plural = _('Product bids')

    def get_absolute_url(self):
        kwargs = {
            'product_slug': self.product.slug,
            'product_pk': self.product.id,
            'pk': self.id
        }
        return reverse('catalogue:bids-detail', kwargs=kwargs)

    def __str__(self):
        return self.product.title

    def clean(self):
        self.user_bid1 = self.user_bid1.strip()
        self.user_bid2 = self.user_bid1.strip()
        self.user_bid3 = self.user_bid1.strip()
        if not self.user and not (self.name and self.email):
            raise ValidationError(
                _("Anonymous bids must include a name and an email"))

    def save(self, *args, **kwargs):
        super(ProductBid, self).save(*args, **kwargs)
        # self.product.update_rating()

    def delete(self, *args, **kwargs):
        super(ProductBid, self).delete(*args, **kwargs)
        # if self.product is not None:
        #     self.product.update_rating()

    # Properties

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def pending_moderation(self):
        return self.status == self.FOR_MODERATION

    @property
    def is_approved(self):
        return self.status == self.APPROVED

    @property
    def is_rejected(self):
        return self.status == self.REJECTED

    # Helpers

   
#  def can_user_vote(self, user):
        """
        Test whether the passed user is allowed to vote on this
        review














        if not user.is_authenticated():
            return False, _(u"Only signed in users can vote")
        vote = self.votes.model(review=self, user=user, delta=1)
        try:
            vote.full_clean()
        except ValidationError as e:
            return False, u"%s" % e
        return True, ""
 """