var app = app || {};

app.GridView = Backbone.View.extend({

    initialize : function() {

        var self = this
        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/grid.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.renderCharts()
            })

        } else {

            self.render()

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template )

        $('.test-div').css('opacity', 1)

    },

    events : {

        "click .exploration-heading" : "toggleContainer",

    },

    renderCharts : function() {

        var self = this

        var hist = new app.Histogram({ el : $('.histogram'), model : { "data" : self.model } })

        var line = new app.LineChart({ el : $('.line-chart'), model : { "data" : self.model } })

        var scatter = new app.ScatterPlot({ el : $('.scatter-plot'), model : { "data" : self.model } })

        var descriptiveStats = new app.DescriptiveStats({ el : $('.descriptive-stats'), model : { "data" : self.model } })

        var subsets = new app.Subsets({ el : $('.subsets'), model : { "data" : self.model } })

        var map = new L.Map('map');

        // create the tile layer with correct attribution
        var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12});

        // start the map in South-East England
        map.setView(new L.LatLng(51.3, 0.7),9);
        map.addLayer(osm);


    },
    // note : should this functionality be in a route?
    toggleContainer : function( ev ){

        console.log("the target is", $(ev.target) )

        var clicked = $(ev.target).parent().attr('id'),
            clickedSelector = '#' + clicked,
            clickedDiv = $(clickedSelector),
            viewName = $(ev.target).html(),
            self = this

        console.log("clicked is", clickedSelector)

        if ( clickedDiv.hasClass('expanded') ) {

            this.contractContainer()        
            self.removeExpandedView( viewName )  
            

        } else {

            console.log("this bitch has been clicked!")

            // console.log("firing")
            $('.test-div').not(clickedSelector).hide()
            //.queue(function(){
            //     console.log("ishould be firing")
            clickedDiv.addClass('expanded')
            // })

            console.log("view name is ", viewName)
            this.createExpandedView( viewName )

        }
        
    },

    createExpandedView : function( viewName ) {

        switch(viewName){
            case "Time":
                var timeseries = new app.TimeseriesView({
                    el : $('.line-chart')
                })
                break;
            case "Space":
                var geospatial = new app.GeospatialView({
                    el : $('.space')
                })
                break;
            case "Two Variables":
                break;
            case "Descriptive Statistics":
                break
            case "Subsets":
                break
        }

    },

    removeExpandedView : function( viewName ){

        var self = this

        switch(viewName){
            case "Time":
                console.log("issa time!")
                $('#timeseries_content_container').remove()
                .delay(1100).queue(function(){
                    var line = new app.LineChart({ 
                        el : $('.line-chart'), 
                        model : { "data" : self.model } 
                    }) 
                })
                break;
            case "Space":
                console.log("issa space!")
                $('#geospatial_content_container').remove()
                .delay(1100).queue(function(){
                    
                    $('#spatial_view').append("<div id='map'></div>")
                    var map = new L.Map('map');

                    // create the tile layer with correct attribution
                    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
                    var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12});       

                    // start the map in South-East England
                    map.setView(new L.LatLng(51.3, 0.7),9);
                    map.addLayer(osm);
                })
                break;
            case "Two Variables":
                break;
            case "Descriptive Statistics":
                break
            case "Subsets":
                break
        }

    },

    contractContainer : function( ev ){

        $('.expanded').removeClass('expanded')
        $('.test-div').show()

    },

    changeActiveAdj : function( ev ) {

        if ( !$(this).hasClass('active-adj') ){

            console.log("changing this than")
             var adjAccent = $(ev.target).html() + '-accent'
             $('.active-adj').removeClass(currentAdj + ' active-adj')
             $(this).addClass(adjAccent + ' active-adj')

        }

    } 

})