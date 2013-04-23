var app = app || {};

app.TimeseriesView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/timeseries.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        $('.line-chart .vis-container').remove()

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.append( template );
        // $('#action_list').hide().fadeIn()

    }, 

    events : {

        "click #chart_type_list li" : "addChartSelection",
        "click #data_type_list li" : "addDataSelection"

    },

    addChartSelection : function(ev){

        var accentClass = $('.active-adj').html() + "-accent"
        $('.selected-chart').removeClass('selected-chart')
        $(ev.target).addClass('selected-chart ' + accentClass)

    },

    addDataSelection : function(ev){

        var accentClass = $('.active-adj').html() + "-accent"
        $('.selected-data').removeClass('selected-data')
        $(ev.target).addClass('selected-chart ' + accentClass)

    },

    populateAttributeDrop : function(){



    },

    addAttribute : function() {


    }

})