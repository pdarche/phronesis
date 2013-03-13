
$(document).ready(function(){

    // var query_view = new QueryView({ el: $("body") });
    var nutrition_view = new app.NutritionView({ el: $("body") });

})


Handlebars.registerHelper('ifCond', function(v, options) {
  console.log(v1)
  if(v !== undefine) {
    return options.fn(this);
  }else{
  	options.fn("No Data")
  }
  
});
    