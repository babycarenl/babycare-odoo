openerp.bbc_crm = function (instance) {
  instance.web.ListView.include({
    load_list: function (data) {
      this._super(data);
      if (this.$buttons) {
        this.$buttons
          .find(".oe_lead_delete")
          .off()
          .click(this.proxy("delete_lead"));
      }
    },
    delete_lead: function () {
      this.do_delete_selected();
    },
  });

  instance.web.FormView.include({
    load_form: function (data) {
      this._super(data);
      if (this.$buttons) {
        this.$buttons
          .find(".oe_lead_delete")
          .off()
          .click(this.proxy("delete_lead"));
      }
    },
    delete_lead: function () {
      this.on_button_delete();
    },
  });
};
