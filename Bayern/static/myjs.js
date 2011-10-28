(function($) {
    $(document).ready(function($) {
      $("#id_transaction_type").change(function() {
	var foo = $("#id_transaction_type option:selected").val();
	if(foo == "En")
	 {
	   $(".piece_price.form-row").show();
	 }
	 else
	 {
	   $(".piece_price.form-row").hide();
	 }
      });
    });
})(django.jQuery);

