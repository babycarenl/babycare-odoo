# -*- coding: utf-8 -*-
from openerp import models, api


class ProductAttributeManager(models.Model):
    _name = 'product.attributemanager'

    @api.multi
    def action_call_magento_sync_all_brands(self):
        self.env['magento.synchronization'].syncAllBrands()

    @api.multi
    def action_call_magento_sync_all_colors(self):
        self.env['magento.synchronization'].syncAllColors()

    @api.multi
    def action_call_magento_sync_all_buggies_agecategory(self):
        self.env['magento.synchronization'].syncAllBuggiesAgeCategory()

    @api.multi
    def action_call_magento_sync_all_buggies_maxcarryweight(self):
        self.env['magento.synchronization'].syncAllBuggiesMaxCarryWeight()

    @api.multi
    def action_call_magento_sync_all_buggies_numberofwheels(self):
        self.env['magento.synchronization'].syncAllBuggiesNumberOfWheels()

    @api.multi
    def action_call_magento_sync_all_carriers_directionofuse(self):
        self.env['magento.synchronization'].syncAllCarriersDirectionOfUse()

    @api.multi
    def action_call_magento_sync_all_carriers_maxcarryweight(self):
        self.env['magento.synchronization'].syncAllCarriersMaxCarryWeight()

    @api.multi
    def action_call_magento_sync_all_carriers_type(self):
        self.env['magento.synchronization'].syncAllCarriersType()

    @api.multi
    def action_call_magento_sync_all_carseats_agecategory(self):
        self.env['magento.synchronization'].syncAllCarSeatsAgeCategory()

    @api.multi
    def action_call_magento_sync_all_carseats_childlength(self):
        self.env['magento.synchronization'].syncAllCarSeatsChildLength()

    @api.multi
    def action_call_magento_sync_all_carseats_childweight(self):
        self.env['magento.synchronization'].syncAllCarSeatsChildWeight()

    @api.multi
    def action_call_magento_sync_all_carseats_directionofuse(self):
        self.env['magento.synchronization'].syncAllCarSeatsDirectionOfUse()

    @api.multi
    def action_call_magento_sync_all_carseats_installmethod(self):
        self.env['magento.synchronization'].syncAllCarSeatsInstallMethod()

    @api.multi
    def action_call_magento_sync_all_clothes_season(self):
        self.env['magento.synchronization'].syncAllClothesSeason()

    @api.multi
    def action_call_magento_sync_all_clothes_size(self):
        self.env['magento.synchronization'].syncAllClothesSize()

    @api.multi
    def action_call_magento_sync_all_highchairs_agecategory(self):
        self.env['magento.synchronization'].syncAllHighChairsAgeCategory()

    @api.multi
    def action_call_magento_sync_all_highchairs_material(self):
        self.env['magento.synchronization'].syncAllHighChairsMaterial()

    @api.multi
    def action_call_magento_sync_all_monitors_maxrange(self):
        self.env['magento.synchronization'].syncAllMonitorsMaxRange()

    @api.multi
    def action_call_magento_sync_all_rockers_maxcarryweight(self):
        self.env['magento.synchronization'].syncAllRockersMaxCarryWeight()

    @api.multi
    def action_call_magento_sync_all_strollers_numberofwheels(self):
        self.env['magento.synchronization'].syncAllStrollersNumberOfWheels()

    @api.multi
    def action_call_magento_sync_all_textiles_size(self):
        self.env['magento.synchronization'].syncAllTextilesSize()

    @api.multi
    def action_call_magento_sync_all_toys_agecategory(self):
        self.env['magento.synchronization'].syncAllToysAgeCategory()

    @api.multi
    def action_call_magento_sync_all_toys_type(self):
        self.env['magento.synchronization'].syncAllToysType()

    @api.multi
    def action_call_magento_sync_all_buggies_adjustablebackrest(self):
        self.env['magento.synchronization'].syncAllBuggiesAdjustableBackrest()

    @api.multi
    def action_call_magento_sync_all_clothes_gender(self):
        self.env['magento.synchronization'].syncAllClothesGender()

    @api.multi
    def action_call_magento_sync_all_highchairs_includingdinnertray(self):
        self.env[
            'magento.synchronization'
        ].syncAllHighChairsIncludingDinnerTray()

    @api.multi
    def action_call_magento_sync_all_highchairs_collapsible(self):
        self.env['magento.synchronization'].syncAllHighChairsCollapsible()

    @api.multi
    def action_call_magento_sync_all_monitors_includingcamera(self):
        self.env['magento.synchronization'].syncAllMonitorsIncludingCamera()

    @api.multi
    def action_call_magento_sync_all_monitors_includingrecallfunction(self):
        self.env[
            'magento.synchronization'
        ].syncAllMonitorsIncludingRecallFunction()

    @api.multi
    def action_call_magento_sync_all_rockers_collapsible(self):
        self.env['magento.synchronization'].syncAllRockersCollapsible()

    @api.multi
    def action_call_magento_sync_all_travelcots_collapsible(self):
        self.env['magento.synchronization'].syncAllTravelcotsCollapsible()

    @api.multi
    def action_call_magento_sync_all_travelcots_includingwheels(self):
        self.env['magento.synchronization'].syncAllTravelcotsIncludingWheels()

    @api.multi
    def action_call_magento_sync_all_travelcots_includingcreephatch(self):
        self.env[
            'magento.synchronization'
        ].syncAllTravelcotsIncludingCreepHatch()
