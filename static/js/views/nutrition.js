NutritionView = Backbone.View.extend({
    
    initialize: function(){
        
        this.render();

    },

    render: function(){

        $.when( 
            $.get('/static/js/templates/nutritionView.handlebars'),
            $.get('/v1/data/pdarche/body/nutrition?order_by=desc')
        )
        .done( 
            function( nutritionView, nutritionData ){ 

                nutritionData = $.parseJSON(nutritionData[0])
                nutritionView = nutritionView[0]

                nutritionData.sort(function(a,b){

                    a = toUTC( a.info.dates.taken )
                    b = toUTC( b.info.dates.taken )
                    return a < b ? - 1 : a > b ? 1 : 0;

                });

                var splitByDate = [],
                    lastDay = 0

                for (var i = 0; i < nutritionData.length - 1; ++i ) {
                    var curr = nutritionData[i+1].info.dates.taken,
                        prev = nutritionData[i].info.dates.taken
                     
                    if ( toUTC( curr ) > toUTC( prev ) ){
                        
                        var date = $.datepicker.formatDate('MM dd, yy', new Date(prev));
                        var newDay = nutritionData.slice(lastDay,i+1)

                        newDay.sort(function(a,b){

                            a = Number(a.info.dates.posted)
                            b = Number(b.info.dates.posted)
                            return a < b ? - 1 : a > b ? 1 : 0;

                        });

                        splitByDate.push({ "date" : date , "meal" : newDay } )
                        lastDay = i + 1

                    } 
                }

                //render templates
                var source = $(nutritionView).html()
                var template = Handlebars.compile( source )
                $('body').append( template( { "day" : splitByDate.reverse() } ) )

            }
        )

    },
    
    events : {

        "click .meal-container" : "blank",
        "click .meal-info-container h2" : "editMealName",
        "click .new-meal-name-submit" : "submitNewMealName"

    },

    toggleMeal : function(ev){

        if ( $(ev.target).hasClass('clicked') ){

            $(ev.target).removeClass('clicked')
        } else {

            $(ev.target).addClass('clicked')
        }

    },

    blank : function() {

    },

    editMealName : function(ev) {
        var currName = { "placeholder" : $(ev.target).html() }

        $.when( 
            $.get('/static/js/templates/mealNamePartial.handlebars') 
        )
        .done(
            function(data){
                var source = $(data).html()
                var template = Handlebars.compile( source )
                $(ev.target).replaceWith( template(currName) )
            }
        )
    },

    submitNewMealName : function(ev){
        var newMealName = $(ev.target).prev().val()

        $(ev.target).parent().replaceWith('<h2>' + newMealName + '</h2>')
    }

});

var toUTC = function( dateString ){
    var dateComponents = dateString.split(" ")[0].split("-"),
    utc = Date.UTC( 
            dateComponents[0], 
            dateComponents[1], 
            dateComponents[2]
        )

    return utc
}

Handlebars.registerHelper('formatTime', function(date) {
  var date = date.fn(this)
  var d = new Date(date),
    hh = d.getHours(),
    m = d.getMinutes(),
    s = d.getSeconds(),
    dd = "AM",
    h = hh

    if (h >= 12) {
        h = hh-12;
        dd = "PM";
    }
    if (h == 0) {
        h = 12;
    }
    m = m<10?"0"+m:m;

    s = s<10?"0"+s:s;

    var pattern = new RegExp("0?"+hh+":"+m+":"+s);

    var replacement = h+":"+m;

    replacement += " "+dd;    

    time = replacement.split(" ")
    
    return time[0] + " " + time[1]
});



//http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg