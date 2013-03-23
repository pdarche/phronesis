var app = app || {};

app.MealView = Backbone.View.extend({
    tagName : 'div',
    className : 'meal-container',

    initialize : function() {

        if ( !($.isFunction(this.template)) ){

            var self = this;    
            $.get('/static/js/templates/meal.handlebars', function(tmpl){
                self.template = tmpl;
                self.render(self.model);
            })

        } else {

            console.log("gots the template");

        }

        this.model.bind('change', _.bind(this.render, this));

    },

    render: function() {

        var model = this.model.toJSON();
        var source = $(this.template).html();
        var template = Handlebars.compile(source);
        this.$el.html(template({ "cid" : this.model.cid, "data" : model }))

        return this
    },

    events : {

        "click h2" : "editMeal"

    },

    editMeal : function( ev ) {

        var model = this.model
        var edit = new app.MealEditView({ el : $('body'), model : model })

    }

})

app.NutritionFacts = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/NutritionFacts.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

        this.model.bind('change', _.bind(this.render, this));

    },

    render : function() {

        var model = this.model.toJSON()
        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( model ) )

    }

})

app.IngredientView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/NutritionFacts.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

        this.model.bind('change', _.bind(this.render, this));

    },
  
})


app.MealEditView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/mealEdit.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

    },

    render: function() {

        var model = this.model.toJSON()
        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        $('body').prepend( template( { "cid" : this.model.cid, "data" : model } ) )

        this.checkMeal()
        this.addFacts()

    },

    events : {

        "click #meal_heading_info_edit h2" : "editMealName",
        "click .new-meal-name-submit" : "setNewMealName",
        "click #search_submit" : "searchIngredient",
        "click #add_ingredient" : "addIngredient",
        "click #backdrop" : "removeEditMeal",
        "click #meal" : "editMeal",
        "click #new_meal_meal_submit" : "setNewMealMeal"

    },

    close : function(){

        $(this.el).undelegate('#meal_heading_info_edit', 'click');
        $(this.el).undelegate('.new-meal-name-submit', 'click');
        $(this.el).undelegate('#search_submit', 'click');
        $(this.el).undelegate('#new_meal_meal_submit', 'click');
        $(this.el).undelegate('#add_ingredient', 'click');
        $(this.el).undelegate('#meal', 'click');
        $(this.el).undelegate('#backdrop', 'click');
        $(this.el).undelegate('.new-meal-name-submit', 'click');

    },

    checkMeal : function(){

        if ( $('#meal').html().length === 0)
            $('#meal').html('no meal indicated').css("font-style", "italic")

    },

    addFacts : function() {

        var self = this
        var facts = new app.NutritionFacts({
            model : self.model,
            el : $('#nutrition_facts')
        })

    },

    editMeal : function(ev) {

        var currName = { "placeholder" : $(ev.target).html() }

        $.when( 
            $.get('/static/js/templates/mealMealPartial.handlebars') 
        )
        .done(
            function(data){
                var source = $(data).html()
                var template = Handlebars.compile( source )
                $(ev.target).replaceWith( template(currName) )
            }
        )

    },

    setNewMealMeal : function(ev) {

        var newMeal = $(ev.target).prev().val()

        this.model.set('meal', newMeal)

        console.log(this.model.attributes)

        $(ev.target).parent().replaceWith('<h3 id="meal">' + newMeal + '</h3>')

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

        var newMealName = $(ev.target).prev().val()

        this.model.set('meal_item_name', newMealName)

        $(ev.target).parent().replaceWith('<h2>' + newMealName + '</h2>')

    },

    searchIngredient : function(ev) {

        var appId = '77751166',
            appKey = '89a33cd92074a64e0cf83f34952d9bf1',
            qString = $(':input').val()

        if ( qString.length > 2 ){

            var url = 'http://api.nutritionix.com/v1/search/'
                url += qString + '?'
                url += 'appId=' + appId + '&appKey=' + appKey
            
            //remove old foods
            $('#ingredients option').remove()

            $.get(url, function(data){

                $.each(data.hits, function(i){ 
                    
                    var html = '<option value="' + this.fields.item_id + '">'
                        html += this.fields.brand_name + ' '
                        html += this.fields.item_name + '</option>'
                    
                    $('#ingredients select').append(html)

                })

            })    

        }
    },

    addIngredient : function(ev){

        var self = this

        var appId = '77751166',
            appKey = '89a33cd92074a64e0cf83f34952d9bf1',
            qString = $(':selected').val()

        var url = 'http://api.nutritionix.com/v1/item/'
            url += qString + '?'
            url += 'appId=' + appId + '&appKey=' + appKey

        $.when( $.get(url ) )
        .done(
            function(data){

                var ingredients = self.model.attributes.ingredients

                ingredients.push( self.createIngredientObj( data ) )
                
                self.updateModelNutritionInfo( data )

            }
        )

    },

    updateModelNutritionInfo : function( nutIxObj ) {

        var calcium = Number(this.model.get('calcium')) + nutIxObj.nf_calcium_dv,
            calories = Number(this.model.get('calories')) + nutIxObj.nf_calories
            calories_from_fat = Number(this.model.get('calories_from_fat')) + nutIxObj.nf_calories_from_fat,
            cholesterol = Number(this.model.get('cholesterol')) + nutIxObj.nf_cholesterol,
            dietary_fiber = Number(this.model.get('dietary_fiber')) + nutIxObj.nf_dietary_fiber,
            protein = Number(this.model.get('protein')) + nutIxObj.nf_protein,
            saturated_fat = Number(this.model.get('saturated_fat')) + nutIxObj.nf_saturated_fat,
            sodium = Number(this.model.get('sodium')) + nutIxObj.nf_sodium,
            sugar = Number(this.model.get('sugar')) + nutIxObj.nf_sugars,
            total_carbs = Number(this.model.get('total_carbs')) + nutIxObj.nf_total_carbohydrate,
            total_fat = Number(this.model.get('total_fat')) + nutIxObj.nf_total_fat,
            trans_fat = Number(this.model.get('trans_fat')) + nutIxObj.nf_trans_fatty_acid,
            vit_a = Number(this.model.get('vit_a')) + nutIxObj.nf_vitamin_a_dv,
            vit_c = Number(this.model.get('vit_c')) + nutIxObj.nf_vitamin_c_dv

        this.model.set({
            'calcium' : calcium,
            'calories' : calories,
            'calories_from_fat' : calories_from_fat,
            'cholesterol' : cholesterol,
            'dietary_fiber' : dietary_fiber,
            'protein' : protein,
            'saturated_fat' : saturated_fat,
            'sodium' : sodium,
            'sugar' : sugar,
            'total_carbs' : total_carbs,
            'total_fat' : total_fat,
            'trans_fat' : trans_fat,
            'vit_a' : vit_a,
            'vit_c' : vit_c
        })

        // this.updateNutritionInfo()

    },

    updateNutritionInfo : function() {

        $('#cals').html(this.model.get('calories'))
        $('#fat').html(this.model.get('total_fat'))
        $('#sat_fat').html(this.model.get('saturated_fat'))
        $('#trans_fat').html(this.model.get('trans_fat'))
        $('#cholesterol').html(this.model.get('cholesterol'))
        $('#sodium').html(this.model.get('sodium'))
        $('#carbs').html(this.model.get('total_carbs'))
        $('#fiber').html(this.model.get('dietary_fiber'))
        $('#sugar').html(this.model.get('sugar'))
        $('#protein').html(this.model.get('protein'))

    },

    createIngredientObj : function( nutIxObj ) {

        var newObj = {
            name : nutIxObj.item_name,
            brand : nutIxObj.brand_name,
            item_description : nutIxObj.item_description,
            ingredient_statement : nutIxObj.nf_ingredient_statement,
            calories : nutIxObj.nf_calories,
            calories_from_fat : nutIxObj.nf_calories_from_fat,
            total_fat : nutIxObj.nf_total_fat,
            monounsaturated_fat : nutIxObj.nf_monounsaturated_fat,
            polyunsaturated_fat : nutIxObj.nf_polyunsaturated_fat,
            saturated_fat : nutIxObj.nf_saturated_fat,
            trans_fat : nutIxObj.nf_trans_fatty_acid,
            cholesterol : nutIxObj.nf_cholesterol,
            sodium : nutIxObj.nf_sodium,
            total_carbs : nutIxObj.nf_total_carbohydrate,
            dietary_fiber : nutIxObj.nf_dietary_fiber,
            sugar : nutIxObj.nf_sugars,
            protein : nutIxObj.nf_protein,
            vit_a_dv : nutIxObj.nf_vitamin_a_dv,
            vit_c_dv : nutIxObj.nf_vitamin_c_dv,
            calcium_dv : nutIxObj.nf_calcium_dv,
            iron_dv : nutIxObj.nf_iron_dv,
            source : "nutritionix",
            refuse_pct : nutIxObj.nf_refuse_pct,
            serving_size_qty : nutIxObj.nf_serving_size_qty,
            serving_size_unit : nutIxObj.nf_serving_size_unit,
            serving_weight_grams : nutIxObj.nf_serving_weight_grams,
            servings_per_container : nutIxObj.nf_servings_per_container,
            water_grams : nutIxObj.nf_water_grams,
            upc : nutIxObj.upc,
            updated_at : nutIxObj.updated_at

        }

        return newObj

    },

    removeEditMeal : function(ev) {
        
        if ( $(ev.target).attr('id') !== 'backdrop' ){

            ev.stopPropagation()

        } else {

            $('#backdrop').remove()
            this.close()
        }

    }    

})



app.NutritionView = Backbone.View.extend({
    
    initialize: function(){

        var self = this;
        this.collection = new Meals()
        this.collection.fetch()
        this.collection.bind("reset", function() { self.render(); });

    },

    render: function(){

        this.collection.each( function( meal ) {
            this.renderMeal(meal)
        }, this )

    },

    renderMeal : function( meal ) {

        var mealView = new app.MealView({
            model : meal
        });

        this.$el.append( mealView.el )

    },
    
    events : {
        
        "click .from" : "editFromLocation"

    },

    editFromLocation : function(ev){

        var cid = $(ev.target).parent().parent().attr('id'),
            model = this.collection.getByCid(cid),
            targetTime = model.get('created_at'),
            startTime = targetTime - 3000,
            endTime = targetTime + 3000,
            url = '/v1/data/pdarche/body/location?created_at__gte=' + startTime
            url += '&created_at__lte=' + endTime + '&source=Foursquare'  

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