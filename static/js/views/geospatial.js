var app = app || {};

app.GeospatialView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.when( $.get('/static/js/templates/geospatial.handlebars'),
                    $.get('/static/js/templates/dataAttributePartial.handlebars'),
                    $.get('/static/js/templates/query.handlebars'))
             .done( function(tmpl1, tmpl2, tmpl3) {
                self.template = tmpl1[0]
                self.attributePartial = tmpl2[0]
                self.queryFilter = tmpl3[0]
                self.render()
                setTimeout(self.renderMap, 1000)
                $('#start_date, #end_date').datepicker()
             })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        $('.space #map').remove()
        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.append( template );

    }, 

    events : {

        "click #data_type_list li" : "addDataSelection",
        "click #add_filter" : "addFilter",
        "click .remove-filter" : "removeFilter",
        "click #submit_query" : "submitQuery",
        "click #clear_map" : "clearMap"

    },

    addDataSelection : function(ev){

        var self = this
        var accentClass = $('.active-adj').html() + "-accent"
        $('.selected-data').removeClass(accentClass).removeClass('selected-data')
        $(ev.target).addClass('selected-data ' + accentClass)

    },

    addFilter : function( refObject ){

        var self = this

        if ($('.selected-data').length) {

            var url = "v1/data/pdarche/body/",
                dataType = $('.selected-data').attr('id')
                url += dataType
                self.currentDataType = dataType

            $.when( $.getJSON(url) )
             .done( 
                function(data){
                    self.renderFilter( data[0] )                
                }
             )

        } else {

            // handle the exception

        }

    },

    renderFilter : function( refObject ){

        var attributes = []
        for ( key in refObject ){
            attributes.push(key)
        }

        var source = $(this.queryFilter).html();
        var template = Handlebars.compile( source );
        $('#filter_list').append( template( { "attribute" : attributes } ) );

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

    removeFilter : function( ev ){

        $(ev.target).parent().remove()
        console.log("the target is", $(ev.target))

    },

    prepData : function( attribute ){

        var self = this
        var data = []
        console.log("the attribute is:", attribute)
        _.each( self[self.currentDataType], function(obj){
            
        })

        return data

    },

    submitQuery : function(){

        var dataType = $('.selected-data').attr('id'),
            startDate = $('#start_date').val(),
            endDate = $('#end_date').val(),
            baseUrl = 'v1/data/pdarche/body/',
            self = this

        baseUrl += dataType + '?'
        startDate !== "" ? baseUrl += "created_at__gte=" + (new Date(startDate).getTime() / 1000) + '&' : null
        endDate !== "" ? baseUrl += "created_at__lte=" + (new Date(endDate).getTime() / 1000) + '&' : null

        var additionalParams = this.additionalParamsString( $('.query-options') )
        baseUrl += additionalParams
        baseUrl = baseUrl.substring(0, baseUrl.length - 1)

        console.log("fetching query", baseUrl)

        $.when( $.getJSON(baseUrl) )
         .done( self.plotData )

    },

    additionalParamsString : function( params ){

        var paramStr = "";

        _.each( params, function( param ){
            
            var parameter = $(param).find('.query-parameter option:selected').val(),
                filter = $(param).find('.query-filter option:selected').val(),
                value = $(param).find('.query-text').val()

                console.log(parameter)

                paramStr += (parameter + "__" + filter + '=' + value + '&')
        
        })

        return paramStr

    },

    plotData : function( locations ){

        var self = this

        _.each( locations, function( location ){
            
            if ( location.from_loc !== null ) {

                var lat = location.from_loc[0],
                    lon = location.from_loc[1],
                    marker = L.marker([lon, lat]).addTo(window.map),
                    locationName = location.meal_item_name,
                    mealUrl = location.img_url
                    time = location.flkr_dates.taken

                    console.log( location )
                    marker.bindPopup("<div>" + locationName + "</div><div>" + time + "</div></div><img src='" + mealUrl +"'/>");

            }
        })

    },

    renderMap : function( data ){

        window.map = new L.Map('vis_container');

        // create the tile layer with correct attribution
        var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osm = new L.TileLayer(osmUrl, {minZoom: 1, maxZoom: 20});       

        // start the map in Brooklyn
        map.setView(new L.LatLng(40.7111,-73.9565), 15);
        map.addLayer(osm);

    },

    clearMap : function(){

        $('.leaflet-marker-icon, .leaflet-marker-shadow, .leaflet-popup-content').remove()

    }

})