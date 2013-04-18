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

        "click .exploration-heading" : "expandContainer",
        "click .expanded" : "contractContainer"

    },

    renderCharts : function() {

        var self = this

        // $.when( 
        //     $.getJSON('v1/data/pdarche/body/physicalActivity?created_at__gte=1357020000&created_at__lte=1365375284')
        // )
        // .done(
        //     function( data ){

                var hist = new app.Histogram({ el : $('.histogram'), model : { "data" : self.model } })

                var line = new app.LineChart({ el : $('.line-chart'), model : { "data" : self.model } })

                var scatter = new app.ScatterPlot({ el : $('.scatter-plot'), model : { "data" : self.model } })

                var descriptiveStats = new app.DescriptiveStats({ el : $('.descriptive-stats'), model : { "data" : self.model } })

                var map = new L.Map('map');

                // create the tile layer with correct attribution
                var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
                var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12});       

                // start the map in South-East England
                map.setView(new L.LatLng(51.3, 0.7),9);
                map.addLayer(osm);

        //     }

        // )

    },

    expandContainer : function( ev ){

        var clicked = $(ev.target).parent()
        $('.test-div').not(clicked).hide().queue(function(){
            clicked.addClass('expanded') 
        })
        
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