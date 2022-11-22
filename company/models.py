from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.translation import pgettext_lazy
from django_countries.fields import Country, CountryField
from django.db.models import Q, Value
from django.utils import timezone
from django.utils.translation import gettext as _
from company.utilities import SlugableModel


class AddressQueryset(models.QuerySet):
    def annotate_default(self, user):
        # Set default shipping/billing address pk to None
        # if default shipping/billing address doesn't exist
        default_shipping_address_pk, default_billing_address_pk = None, None
        if user.default_shipping_address:
            default_shipping_address_pk = user.default_shipping_address.pk
        if user.default_billing_address:
            default_billing_address_pk = user.default_billing_address.pk

        return user.addresses.annotate(
            user_default_shipping_address_pk=Value(
                default_shipping_address_pk, models.IntegerField()
            ),
            user_default_billing_address_pk=Value(
                default_billing_address_pk, models.IntegerField()
            ),
        )


class Address(SlugableModel):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=10, blank=True, default="")

    objects = AddressQueryset.as_manager()

    class Meta:
        ordering = ("pk",)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        if self.company_name:
            return "%s - %s" % (self.company_name, self.full_name)
        return self.full_name

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data() == other.as_data()

    __hash__ = models.Model.__hash__


    def get_copy(self):
        """Return a new instance of the same address."""
        return Address.objects.create(**self.as_data())

class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def customers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(orders__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)



class User(PermissionsMixin, AbstractBaseUser, SlugableModel):
    """
    1 - admin will only be the owner of the SAAS
    2 - shop owner is the user linked to the company that pays for the saas
    3 - shop employee will be the user employed by the client company ( shop owner )
    4 - client will be the people consuming the end service
    """

    USER_TYPE = (
        ("admin", _("admin")),
        ("owner", _("owner")),
        ("employee", _("employee")),
        ("client", _("client")),
        ("unset", _("unset"))
    )
    user_type = models.CharField(choices=USER_TYPE, default="owner", max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar', blank=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        permissions = (
            (
                "manage_users",
                pgettext_lazy("Permission description", "Manage customers."),
            ),
            ("manage_staff", pgettext_lazy("Permission description", "Manage staff.")),
            (
                "impersonate_users",
                pgettext_lazy("Permission description", "Impersonate customers."),
            ),
        )

    def __str__(self):
        return str(self.first_name) or ""

    def get_agnostic_included_fields(self):
        return ["email", "first_name", "last_name", "avatar"]

    def get_agnostic_special_fields(self):
        return []

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        if self.address:
            first_name = self.address.first_name
            last_name = self.address.last_name
            if first_name or last_name:
                return ("%s %s" % (first_name, last_name)).strip()
        return self.email

    def get_absolute_edit_url(self):
        if self.is_staff:
            return reverse("staff:staff-edit", kwargs={
                'slug': self.slug
            })
        else:
            return reverse("customer:customer-update", kwargs={
                'slug': self.slug
            })

    def get_short_name(self):
        return self.email

    def get_ajax_label(self):
        address = self.default_billing_address
        if address:
            return "%s %s (%s)" % (address.first_name, address.last_name, self.email)
        return self.email

class Company(SlugableModel):

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("companies")

    # this is the company which is the client attached to the account
    # do not overwrite the save method as it lives in the SlugableModel

    rpps = models.CharField(max_length=11, blank=True)
    adeli = models.CharField(max_length=11, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    date_of_birth = models.DateTimeField(null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, default="")
    telephone = models.CharField(max_length=10, blank=True, default="")
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}" or ""

    def get_absolute_url(self):
        return reverse(
                    "company:company-detail",
                    kwargs={"slug": self.slug}
                   )

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        if self.address:
            first_name = self.address.first_name
            last_name = self.address.last_name
            if first_name or last_name:
                return ("%s %s" % (first_name, last_name)).strip()
        return self.email

class StoreImages(SlugableModel):


    class Meta:
        verbose_name = "Store Image"
        verbose_name_plural = "Store Images"

    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="pictures")
    logo = models.ImageField(upload_to='shop/logo', blank=True)
    front = models.ImageField(upload_to='shop/front', blank=True)
    inside = models.ImageField(upload_to='shop/inside', blank=True)


    def __str__(self):
        return f"{self.company}" or ""