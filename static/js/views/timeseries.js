var app = app || {};

app.TimeseriesView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.when( $.get('/static/js/templates/timeseries.handlebars'),
                    $.get('/static/js/templates/dataAttributePartial.handlebars'))
             .done( function(tmpl1, tmpl2) {
                self.template = tmpl1[0]
                self.attributePartial = tmpl2[0]
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

    }, 

    events : {

        "click #chart_type_list li" : "addChartSelection",
        "click #data_type_list li" : "addDataSelection",
        "click #add_attribute" : "addAttribute",
        "click .remove-attribute" : "removeAttribute"

    },

    addChartSelection : function(ev){

        var accentClass = $('.active-adj').html() + "-accent"
        $('.selected-chart').removeClass(accentClass).removeClass('selected-chart ')
        $(ev.target).addClass('selected-chart ' + accentClass)
        this.currentChartType = $('.selected-chart').html()

    },

    addDataSelection : function(ev){

        var self = this
        var accentClass = $('.active-adj').html() + "-accent"
        $('.selected-data').removeClass(accentClass).removeClass('selected-data')
        $(ev.target).addClass('selected-data ' + accentClass)

        if ($('.selected-chart').length) {

            var url = "v1/data/pdarche/body/",
                dataType = $('.selected-data').attr('id')
                url += dataType
                self.currentDataType = dataType

            $.when( $.getJSON(url) )
             .done( 
                function(data){
                    console.log(data)
                    data.sort(function(a,b) { return parseInt(a.created_at) - parseInt(b.created_at) } );
                    self[dataType] ? null : self[dataType] = data
                    $('#attribute_drop option').remove()
                    self.populateAttributeDrop( data[0] )
                    console.log("current data type", self.currentDataType)
                }
             )

        } else {

            // handle the exception

        }

    },

    populateAttributeDrop : function( refObject ){

        for ( key in refObject ){

            var option = "<option id='" + key + "' value='" + key + "'>" + key + "</option>"
            $('#attribute_drop').append(option)

        }

    },

    addAttribute : function() {

        var selected = $('#attribute_drop option:selected').text().trim(),
            data = { "attribute_name" : selected },
            self = this
        var source = $(this.attributePartial).html();
        var template = Handlebars.compile( source );
        $('#attribute_list').append( template( data ) );

        var preppedData = self.prepData( selected )
        this.renderChart( preppedData )

    },

    removeAttribute : function( ev ) {

        $(ev.target).parent().remove()

    },

    prepData : function( attribute ){
        
        var self = this        
        var data = []
        console.log("the attribute is:", attribute)
        _.each( self[self.currentDataType], function(obj){        
            data.push( { "date" : obj.created_at, "value" : obj[attribute] })
        })

        return data 

    },

    renderChart : function( data ){

        switch(this.currentChartType){
            case "Line":
                var lineChart = new app.LineChartWithContext({
                    el : $('#vis_container'),
                    model : data
                })
                break;
            case "Space":
                break;
            case "Two Variables":
                break;
            case "Descriptive Statistics":
                break
            case "Subsets":
                break
        }

    }

})