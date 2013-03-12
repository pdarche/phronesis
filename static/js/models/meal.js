 var Meal = Backbone.Model.extend({
        defaults: {
            phro_created_at : undefined,
            username : "pdarche",
            flkr_ref_info : {
                photo_id : undefined,
                farm : undefined,
                server : undefined,
                secret : undefined
            },
            flkr_dates : {
                taken : undefined,
                last_update : undefined,
                taken_granularity : undefined
            },
            meal_item_name : undefined,
            img_url : undefined,
            meal : undefined,
            venue : undefined,
            venue_category : undefined,
            from_loc : [],
            eaten_loc : undefined,
            unit : undefined,
            calories : undefined,
            calories_from_fat : undefined,
            total_fat : undefined,
            saturated_fat : undefined,
            trans_fat : undefined,
            cholesterol : undefined,
            sodium : undefined,
            total_carbs : undefined,
            dietary_fiber : undefined,
            sugar : undefined,
            protein : undefined,
            vit_a : undefined,
            vit_c : undefined,
            calcium : undefined,
            iron : undefined,
            source : undefined, 
            ingredients : []
        },
        initialize: function(){
            this.on("change:meal_item_name", function(model){
                var name = model.get("meal_item_name"); // 'Stewie Griffin'
                console.log("Changed my name to " + name );
            });
        }
});

var Meals = Backbone.Collection.extend({
    model: Meal,
    url : '/v1/data/pdarche/body/nutrition?order_by=desc'
});


       // $.when( 
        //     $.get('/static/js/templates/nutritionView.handlebars')
        // )
        // .done( 
        //     function( nutritionView ){ 
                
        //         nutritionView = nutritionView[0]

        //         collection.models.sort(function(a,b){

        //             a = toUTC( a.attributes.flkr_dates.taken )
        //             b = toUTC( b.attributes.flkr_dates.taken )
        //             return a < b ? - 1 : a > b ? 1 : 0;

        //         });

                // var splitByDate = [],
                //     lastDay = 0

                // for (var i = 0; i < collection.length - 1; ++i ) {
                //     var curr = collection.models[i+1].flkr_dates.taken,
                //         prev = collection.models[i].flkr_dates.taken
                     
                //     if ( toUTC( curr ) > toUTC( prev ) ){
                        
                //         var date = $.datepicker.formatDate('MM dd, yy', new Date(prev));
                //         var newDay = nutritionData.slice(lastDay,i+1)

                //         newDay.sort(function(a,b){

                //             a = Number(a.attributes.flkr_dates.posted)
                //             b = Number(b.attributes.flkr_dates.posted)
                //             return a < b ? - 1 : a > b ? 1 : 0;

                //         });

                //         splitByDate.push({ "date" : date , "meal" : newDay } )
                //         lastDay = i + 1

                //     } 
                // }

                //render templates
                // var source = $(nutritionView).html()
                // var template = Handlebars.compile( source )
                // $('body').append( template( { "day" : collection.models } ) )

        //     }
        // )

