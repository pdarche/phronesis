var app = app || {};

app.PieChart = Backbone.View.extend({
    tagName : 'div',
    className : 'pie-chart-container',
    id : undefined,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/histogram.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.$el.attr( 'id', 'histogram_' + $('.histogram-container').length )
                var idSelector = '#' + self.$el.attr('id') 

                $(idSelector).draggable().resizable({
                    stop : function() {
                        self.renderChart( self )
                    }
                })

                self.renderChart( self )

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var attributes = []

        for ( attr in categoryAttributes[this.model.attribute] ) {
             attributes.push({ 
                title : attr, 
                id : categoryAttributes[this.model.attribute][attr] 
            })
        }

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "attribute" : attributes } ) )

        if ( this.model.attribute === "physicalActivity"){
            $('#steps').addClass('data-source')
        } else if ( this.model.attribute === "sleep"){
            $('#total_z').addClass('data-source')
        } else {
            $('#calories').addClass('data-source')
        }

    },

    events : {

        "click .destroy" : "removeChart",
        "click .record-attribute" : "changeDataSource",

    },

    renderChart : function( self ) {

        var data = this.prepData()

        var margin = {top: 10, right: 30, bottom: 30, left: 30},
            width = this.$el.width() - margin.left - margin.right,
            height = this.$el.height() - $('.destroy').height() - 50 - margin.top - margin.bottom,
            radius = Math.min(width, height) / 2;

        var idSelector = '#' + this.$el.attr('id')

        d3.select(idSelector).select('svg').remove()

        var color = d3.scale.ordinal()
            .range(colorbrewer.Blues[9]);

        var arc = d3.svg.arc()
            .outerRadius(radius - 10)
            .innerRadius(0);

        var pie = d3.layout.pie()
            .sort(null)
            .value(function(d) { return d.value; });

        var svg = d3.select(idSelector).append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        data.forEach(function(d) {
        d.value = +d.value;
        });

        var g = svg.selectAll(".arc")
          .data(pie(data))
        .enter().append("g")
          .attr("class", "arc");

        g.append("path")
          .attr("d", arc)
          .style("fill", function(d) { return color(d.data.name); });

        g.append("text")
          .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
          .attr("dy", ".35em")
          .style("text-anchor", "middle")
          .text(function(d) { return d.data.name; });

    },

    prepData : function(){

        var self = this,
            data = [],
            avgs = []

        var category = this.model.attribute

        _.each( pieValues[category], function(val){
            var attr = []
            _.each( self.model.records, function(obj){
                if( obj[val] !== null ){
                    attr.push(obj[val])
                }
            })

            data.push(attr)
        })

        _.each( data, function(ar, i){
            var sum = _.reduce(ar, function(memo, num){ return memo + num; }, 0 )
            avgs.push( { "name" : pieValues[category][i], "value" : sum/ar.length } )


        })

        console.log(avgs)
        return avgs

    },

    changeDataSource : function( ev ) {
        var self = this

        $('.data-source').removeClass('data-source')
        $(ev.target).addClass('data-source')
        self.renderChart( self )

        // $.when( $('.data-source').removeClass('data-source'))
        // .done(
        //     function(){
        //         $(ev.target).addClass('data-source')
        //         console.log("the target is ", ev.target)
        //         self.renderChart( self )
        //     }
        // )

    },

    removeChart : function(){

        this.$el.remove()

    }

})