from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from ebs.models.master_data_facilities import Tank, Staff
from ebs.models.master_data_products import Product
from ebs.models.master_data_rawmaterials import Material


###
# Schedule Pattern definition.  Note that a schedule pattern
# defines reasonably generic process steps along with the number
# of days offset FROM START that we'd predict that process
# step to be completed.  It is well-understod that every brewery
# will have fine-grained process controls that are not covered by
# these steps, but it is also well-understood that being too
# prescriptive in the process increases implementation time and
# decreases compliance since *everything* is modeled in the process.
#
# In the brewerlean model, we opt for a series of higher-level
# process steps that should be generic enough so as to not interfere
# with local preferences.
class SchedulePattern(models.Model):
    class Meta:
        ordering = ['pattern_name']
        verbose_name_plural = 'Schedule Patterns'

    pattern_name = models.CharField(max_length=25,
                                    verbose_name='Pattern Name')
    pattern_total_days = models.IntegerField(null=True,
                                             verbose_name='Number of Days in the Pattern')
    offset_yeast_crash = models.IntegerField(null=True,
                                             verbose_name='Days Offset for Yeast Crash')
    offset_yeast_harvest = models.IntegerField(null=True,
                                               verbose_name='Days Offset for Yeast Harvest')
    offset_dryhop = models.IntegerField(null=True,
                                        verbose_name='Days Offset for Dry Hop')
    offset_final_crash = models.IntegerField(null=True,
                                             verbose_name='Days Offset for Final Crash')
    offset_transfer = models.IntegerField(null=True,
                                          verbose_name='Days Offset for Transfer')
    offset_package = models.IntegerField(null=True,
                                         verbose_name='Days Offset for Package')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        return self.pattern_name


###
# Unique project sizes
class BatchSize(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Sizes'

    batch_size_name = models.CharField(max_length=25)

    def __str__(self):
        return self.batch_size_name


###
# Defining model for a 'batch', where a batch is a single
# fermenter, but not necessarily a single brite.  Turn numbers
# and day numbers are *hard coded* at the moment, since this
# seems like a minor detail to bother with additional tables
# and most smaller breweries don't run 24hr schedules.
class Batch(models.Model):
    TURN_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4))
    DAY_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4))

    class BatchStatus(models.TextChoices):
        PLANNING = 'PL', 'Planning'
        INPROCESS = 'IP', 'In Process'
        ARCHIVE = 'AR', 'Archive'

    class Meta:
        verbose_name_plural = 'Batches'

    batch_product = models.ForeignKey(Product,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name='Product')
    brewer = models.ForeignKey(Staff,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Brewer')
    status = models.CharField(max_length=2,
                              choices=BatchStatus.choices,
                              default=BatchStatus.PLANNING)
    total_batch_size = models.ForeignKey(BatchSize,
                                         null=True,
                                         blank=True,
                                         on_delete=models.SET_NULL,
                                         verbose_name='Total Volume (BBLs)')
    schedule_pattern = models.ForeignKey(SchedulePattern,
                                         null=True,
                                         blank=True,
                                         on_delete=models.SET_NULL,
                                         verbose_name='Schedule Pattern')
    plan_start_day = models.DateField(default=datetime.now,
                                      verbose_name='Planned Start Date')
    qty_turns = models.IntegerField(null=True,
                                    blank=True,
                                    choices=TURN_CHOICES,
                                    verbose_name='Number of Turns')
    qty_brew_days = models.IntegerField(null=True,
                                        blank=True,
                                        choices=DAY_CHOICES,
                                        verbose_name='Number of Brew Days')
    is_dh = models.BooleanField(verbose_name='Is is Dry-Hopped?',
                                null=True,
                                blank=True,
                                default=False)
    qty_dh_days = models.IntegerField(null=True,
                                      blank=True,
                                      verbose_name='How Many DH Days')
    target_fv = models.ForeignKey(Tank,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name='+',
                                  verbose_name='Target Fermenter')
    target_bt = models.ForeignKey(Tank,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name='+',
                                  verbose_name='Target Brite')
    obeer_batch = models.IntegerField(null=True,
                                      blank=True,
                                      verbose_name='OBeer Batch #')
    obeer_mpn = models.IntegerField(null=True,
                                    blank=True,
                                    verbose_name='OBeer MPN')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.obeer_batch is not None:
            return_name = self.batch_product.ownership.partner_name \
                          + '::' + self.batch_product.product_name + '::' \
                          + self.obeer_batch.__str__()
        else:
            return_name = self.batch_product.ownership.partner_name \
                          + '::' + self.batch_product.product_name \
                          + '::NO BATCH'
        return return_name


###
# New for '23, moving batch package plans into
# ebs.  In this structure it is HIGHLY ENCOURAGED
# for users to enter batch package plans as part
# of the upcoming batch process.  In this way, a
# forward-looking pressure on inventory can be easily
# calculated.
class BatchPackagePlan(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Package Plans'

    batch = models.OneToOneField(Batch,
                             null=True,
                             on_delete=models.SET_NULL,
                                related_name='package_plan')
    kg_half_owned = models.IntegerField(default=0)
    kg_half_oneway = models.IntegerField(default=0)
    kg_half_client = models.IntegerField(default=0)
    kg_half_client_oneway = models.IntegerField(default=0)
    kg_sixth_owned = models.IntegerField(default=0)
    kg_sixth_oneway = models.IntegerField(default=0)
    kg_sixth_client = models.IntegerField(default=0)
    kg_sixth_client_oneway = models.IntegerField(default=0)
    cs_16oz = models.IntegerField(default=0)
    cs_12oz = models.IntegerField(default=0)
    cs_500ml = models.IntegerField(default=0)
    cs_750ml = models.IntegerField(default=0)
    package_note = models.TextField(null=True,
                                    blank=True,
                                    max_length=500)


###
# Plan dates are calculated by the associated view when a
# planned batch is scheduled, based on teh schedule pattern
# that is applied.
class BatchPlanDates(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Plan Dates'

    batch = models.OneToOneField(Batch,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='dates')
    brew_date = models.DateField(null=True,
                                 verbose_name='Plan Brew Date')
    yeast_crash_date = models.DateField(null=True,
                                        verbose_name='Plan Yeast Crash Date')
    yeast_harvest_date = models.DateField(null=True,
                                          verbose_name='Plan Yeast Harvest Date')
    dryhop_date = models.DateField(null=True,
                                   verbose_name='Plan DH Date')
    final_crash_date = models.DateField(null=True,
                                        verbose_name='Plan Final Crash Date')
    transfer_date = models.DateField(null=True,
                                     verbose_name='Plan Transfer Date')
    package_date = models.DateField(null=True,
                                    verbose_name='Plan Package Date')

    @classmethod
    def create(cls, batch):
        plan_rtn = cls(batch=batch)
        return plan_rtn

    def __str__(self):
        return self.brew_date.__str__()


###
# Batch actual dates track actual performance.  In early
# versions this was manually filled in.
class BatchActualDates(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Actual Dates'

    batch = models.ForeignKey(Batch,
                              null=True,
                              on_delete=models.SET_NULL)
    brew_date = models.DateField(null=True,
                                 blank=True,
                                 verbose_name='Actual Brew Date')
    yeast_crash_date = models.DateField(null=True,
                                        blank=True,
                                        verbose_name='Actual Yeast Crash Date')
    yeast_harvest_date = models.DateField(null=True,
                                          blank=True,
                                          verbose_name='Actual Yeast Harvest Date')
    dryhop_date = models.DateField(null=True,
                                   blank=True,
                                   verbose_name='Actual DH Date')
    final_crash_date = models.DateField(null=True,
                                        blank=True,
                                        verbose_name='Actual Final Crash Date')
    transfer_date = models.DateField(null=True,
                                     blank=True,
                                     verbose_name='Actual Transfer Date')
    package_date = models.DateField(null=True,
                                    blank=True,
                                    verbose_name='Actual Package Date')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    @classmethod
    def create(cls, batch):
        act_rtn = cls(batch=batch)
        return act_rtn

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH'
        return return_name


###
# A full list of all the raw materials that were used in any
# particular batch.
class BatchRawMaterialsLog(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Raw Materials Logs'

    batch = models.ForeignKey(Batch,
                              null=True,
                              on_delete=models.SET_NULL)
    material = models.ForeignKey(Material,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Raw Material')
    material_qty = models.CharField(max_length=25,
                                    null=True,
                                    verbose_name='Quantity')
    material_lot = models.CharField(max_length=100,
                                    null=True,
                                    blank=True,
                                    verbose_name='Lot Number')
    is_dh = models.BooleanField(null=True,
                                blank=True,
                                default=False,
                                verbose_name='Is Cold Side?')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__() \
                          + '::' + self.material.material_name
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH' \
                          + '::' + self.material.material_name
        return return_name


###
# Key wort QC items
class BatchWortQC(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Wort QC Data'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    brewer = models.ForeignKey(Staff,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Brewer')
    turn = models.IntegerField(null=True,
                               blank=True,
                               verbose_name='Turn No.')
    temp_mash = models.DecimalField(max_digits=4,
                                    decimal_places=1,
                                    null=True,
                                    blank=True,
                                    verbose_name='Mash Temp')
    ph_mash = models.DecimalField(max_digits=3,
                                  decimal_places=2,
                                  null=True,
                                  blank=True,
                                  verbose_name='Mash pH')
    volume_strike = models.DecimalField(max_digits=3,
                                        decimal_places=0,
                                        null=True,
                                        blank=True,
                                        verbose_name='Strike Water Volume')
    volume_sparge = models.DecimalField(max_digits=3,
                                        decimal_places=0,
                                        null=True,
                                        blank=True,
                                        verbose_name='Sparge Water Volume')
    volume_preboil = models.DecimalField(max_digits=3,
                                         decimal_places=0,
                                         null=True,
                                         blank=True,
                                         verbose_name='Pre-boil Volume')
    volume_postboil = models.DecimalField(max_digits=3,
                                          decimal_places=0,
                                          null=True,
                                          blank=True,
                                          verbose_name='Post-boil Volume')
    extract_first_runnings = models.DecimalField(max_digits=3,
                                                 decimal_places=1,
                                                 null=True,
                                                 blank=True,
                                                 verbose_name='First Runnings P')
    extract_last_runnings = models.DecimalField(max_digits=3,
                                                decimal_places=1,
                                                null=True,
                                                blank=True,
                                                verbose_name='Last runnings P')
    extract_preboil = models.DecimalField(max_digits=3,
                                          decimal_places=1,
                                          null=True,
                                          blank=True,
                                          verbose_name='Pre-Boil P')
    extract_postboil = models.DecimalField(max_digits=3,
                                           decimal_places=1,
                                           null=True,
                                           blank=True,
                                           verbose_name='Post-Boil P')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__() \
                          + '::' + self.turn.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH' \
                          + '::' + self.turn.__str__()
        return return_name


###
# Basic yeast pitch information, related to in-stock materials.
# this will be deprecated eventually by a yeast management
# module.
class BatchYeastPitch(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Yeast Pitches'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff,
                              null=True,
                              on_delete=models.SET_NULL,
                              blank=True,
                              verbose_name='Who Pitched?')
    yeast = models.ForeignKey(Material,
                              null=True,
                              on_delete=models.SET_NULL,
                              blank=True,
                              verbose_name='Yeast')
    yeast_qty = models.CharField(max_length=100,
                                 null=True,
                                 blank=True,
                                 verbose_name='Quantity')
    yeast_source = models.CharField(max_length=100,
                                    null=True,
                                    blank=True,
                                    verbose_name='Source')
    yeast_pitch_temp = models.DecimalField(max_digits=3,
                                           null=True,
                                           decimal_places=1,
                                           blank=True,
                                           verbose_name='Pitch Temp')
    yeast_pitch_turn = models.IntegerField(null=True,
                                           blank=True,
                                           verbose_name='Pitch on Turn')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__() \
                          + '::' + self.yeast.material_name
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH' \
                          + '::' + self.yeast.material_name
        return return_name


###
# Daily fermentation QC log, with extract (calculated and real,
# usable for various methods), temps, and pHs
class BatchFermentationQC(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Fermentation QC Data'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True)
    staff = models.ForeignKey(Staff,
                              null=True,
                              on_delete=models.SET_NULL,
                              blank=True,
                              verbose_name='Who')
    extract_apparent = models.DecimalField(max_digits=3,
                                           decimal_places=1,
                                           null=True,
                                           verbose_name='Apparent Extract')
    sg_real_calculated = models.DecimalField(max_digits=4,
                                             decimal_places=3,
                                             null=True,
                                             blank=True,
                                             verbose_name='Calculated SG')
    ph = models.DecimalField(max_digits=3,
                             decimal_places=2,
                             null=True,
                             blank=True,
                             verbose_name='Current pH')
    temp_sv = models.DecimalField(max_digits=4,
                                  decimal_places=1,
                                  null=True,
                                  blank=True,
                                  verbose_name='Temp Set Value')
    temp_pv = models.DecimalField(max_digits=4,
                                  decimal_places=1,
                                  null=True,
                                  blank=True,
                                  verbose_name='Temp Process Value')
    extract_real = models.DecimalField(max_digits=3,
                                       decimal_places=1,
                                       null=True,
                                       blank=True,
                                       verbose_name='Calculated Real Extract')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__() \
                          + '::' + self.date.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH' \
                          + '::' + self.date.__str__()
        return return_name


###
# Dissolved Oxygen entries at some number of places
# in the process.  Once again, these are hard-coded
# since it seemed odd to make this a configuration.
class BatchDOEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Batch DO Entries'

    class DOType(models.TextChoices):
        PREFERM = 'PE', 'Pre-Fermentation'
        POSTFERM = 'PT', 'Post-Fermentation'
        POSTDRYHOP = 'PD', 'Post Dry-Hop'
        ENDOFFERM = 'PF', 'Post-Fermentation'
        TRANSFER = 'TR', 'Transfer'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    do_type = models.CharField(max_length=2,
                               choices=DOType.choices,
                               default=DOType.PREFERM,
                               verbose_name='D.O. Measurement Type')
    do_measurement = models.CharField(max_length=25,
                                      null=True,
                                      blank=True,
                                      verbose_name='D.O. Value')
    staff = models.ForeignKey(Staff,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Who')
    date = models.DateField(null=True,
                            verbose_name='Date')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__() \
                          + '::' + self.do_type
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH' \
                          + '::' + self.do_type
        return return_name


###
# FV->BT transfer record, volume in gallons.
class BatchTransfer(models.Model):
    class Meta:
        verbose_name_plural = 'Batch Transfers'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Who')
    date = models.DateField(null=True,
                            verbose_name='Date')
    volume_transfer_approx = models.DecimalField(max_digits=4,
                                                 decimal_places=1,
                                                 verbose_name='Approximate Transfer Volume')
    to_tank = models.ForeignKey(Tank,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='To Tank')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH'
        return return_name


###
# Carbonation entry, in volumes
class CarbonationQCEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Carbonation QC Entries'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Who')
    date = models.DateField(null=True,
                            verbose_name='Date')
    carb_vols_brite = models.DecimalField(max_digits=3,
                                          decimal_places=2,
                                          null=True,
                                          blank=True,
                                          verbose_name='Brite Tank Carb Vols')
    last_modified_on = models.DateField(auto_now=True, blank=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH'
        return return_name


###
# A packaging run is a summary of the number of half barrels
# sixtels and cases that were filled, along with the number
# of skids used for each
class PackagingRun(models.Model):
    class Meta:
        verbose_name_plural = 'Packaging Runs'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Who')
    date = models.DateField(null=True,
                            verbose_name='Date')
    filled_halfs = models.IntegerField(null=True,
                                       blank=True,
                                       verbose_name='No. Halfs')
    filled_sixtels = models.IntegerField(null=True,
                                         blank=True,
                                         verbose_name='No. Sixtels')
    skids_kegs = models.IntegerField(null=True,
                                     blank=True,
                                     verbose_name='No. Keg Skids')
    filled_cases = models.IntegerField(null=True,
                                       blank=True,
                                       verbose_name='No. Cases')
    skids_cases = models.IntegerField(null=True,
                                      blank=True,
                                      verbose_name='No. Case Skids')
    line_count = models.IntegerField(null=True,
                                     blank=True,
                                     verbose_name='Line Can Count')
    last_modified_on = models.DateField(auto_now=True, blank=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH'
        return return_name


###
# Canning QC is comprised of relevant measurements
# made by a canning line operator.  Again, these measurements
# types are hard coded, since it seems odd to make them
# a more complicated configuration.
class CanningQC(models.Model):
    class Meta:
        verbose_name_plural = 'Canning QC Data'

    class CanQCType(models.TextChoices):
        WEIGHT = 'WT', 'Weight'
        SEAM_HEIGHT = 'SH', 'Seam Height'
        SEAM_WIDTH = 'SW', 'Seam Width'
        BODY_HOOK = 'BH', 'Body Hook'
        COVER_HOOK = 'CH', 'Cover Hook'
        CAN_DO = 'DO', 'D.O.'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Who')
    date = models.DateField(null=True,
                            verbose_name='Date')
    type = models.CharField(null=True,
                            max_length=2,
                            verbose_name='Type',
                            blank=True,
                            choices=CanQCType.choices,
                            default=CanQCType.WEIGHT)
    measurement = models.DecimalField(max_digits=7,
                                      decimal_places=4,
                                      null=True,
                                      blank=True,
                                      verbose_name='Measurement')
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH'
        return return_name


###
# A note is a random bit of infomration about a batch.  Notes that are
# private are notes that don't get printed on certain reports (say,
# if you are a contract brewer and you publish information that you don't
# want a client to see).  Unlisted Material notes are for adding info
# about raw materials that weren't in the materials list or couldn't easily
# be found--so that prodution staff may continue as normal.
class BatchNote(models.Model):
    class NoteType(models.TextChoices):
        PRIVATE = 'PV', 'Private'
        PUBLIC = 'PB', 'Public'
        UNLISTED_MATERIAL = 'UM', 'Unlisted Material'

    class Meta:
        verbose_name_plural = 'Batch Notes'

    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    note_type = models.CharField(null=True,
                                 max_length=2,
                                 verbose_name='Type',
                                 blank=True,
                                 choices=NoteType.choices,
                                 default=NoteType.PRIVATE)
    note = models.TextField(null=True,
                            blank=True,
                            max_length=500)
    last_modified_on = models.DateField(auto_now=True)
    last_modified_by = models.ForeignKey(User,
                                         null=True,
                                         on_delete=models.SET_NULL,
                                         default=1)

    def __str__(self):
        if self.batch.obeer_batch is not None:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::' + self.batch.obeer_batch.__str__()
        else:
            return_name = self.batch.batch_product.ownership.partner_name \
                          + '::' + self.batch.batch_product.product_name \
                          + '::NO BATCH'
        return return_name
