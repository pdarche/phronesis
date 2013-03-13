var app = app || {};

app.MealView = new Backbone.View.extend({
    tagName: 'div',
    className: 'meal',
    template: _.template( '<div><%=meal_item_name%></div>' ),

    render: function() {

        //tmpl is a function that takes a JSON object and returns html
        var tmpl = this.template

        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( tmpl( this.model.toJSON() ) );

        return this;
    }
})

app.NutritionView = Backbone.View.extend({
    
    initialize: function(){

        this.collection = new Meals()
        this.collection.fetch()
        var self = this;
        this.collection.bind("reset", function() { self.render(); });

    },

    render: function(){
         _.each( this.collection.models, function( item ) {
            this.renderMeal( item );
        }, this );
    },

    renderMeal : function( item ) {

        $.when( $.get('/static/js/templates/meal.handlebars') )
        .done(
            function(data){
                var source = $(data).html()
                var template = Handlebars.compile( source )
                var d = { "id" : item.cid, "data" : item.toJSON() }
                $('#meals_container').append( template( d ) )
            }
        )
        // var mealView = new app.MealView({
        //     model : item
        // });
        // this.$el.append( mealView.render().el );
    },
    
    events : {

        "click .meal-container" : "blank",
        "click .meal-info-container h2" : "editMealName",
        "click .new-meal-name-submit" : "setNewMealName",
        "click .from" : "editFromLocation",
        "keypress :input" : "searchFromLocation"

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

    setNewMealName : function(ev){
        var newMealName = $(ev.target).prev().val(),
            cid = $(ev.target).parent().parent().parent().attr('id'),
            model = this.collection.getByCid(cid)

        model.set('meal_item_name', newMealName)

        $(ev.target).parent().replaceWith('<h2>' + newMealName + '</h2>')

    },

    editFromLocation : function(ev){

        var cid = $(ev.target).parent().parent().attr('id'),
            model = this.collection.getByCid(cid),
            targetTime = model.get('created_at'),
            startTime = targetTime - 3000,
            endTime = targetTime + 3000,
            url = '/v1/data/pdarche/body/location?created_at__gte=' + startTime
            url += '&created_at__lte=' + endTime + '&source=Foursquare'  

        console.log(model.attributes)

        $.when( 
            $.get('/static/js/templates/from.handlebars'),
            $.get( url )
        )
        .done(
            function(template, data){
                var tmpl = template[0],
                    data = $.parseJSON(data[0])

                var source = $(tmpl).html()
                var template = Handlebars.compile( source )
                $(ev.target).replaceWith( template( { "location" : data } ) )
            }
        )

    },

    searchFromLocation : function(ev){

        

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