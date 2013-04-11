var app = app || {};

app.ScatterPlot = Backbone.View.extend({
    tagName : 'div',
    className : 'scatter-plot-container',

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/histogram.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.renderChart( self )

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.append( template )

    },

    events : {

        "click .destroy" : "removeChart",
        "click .record-attribute" : "changeDataSource",

    },

    renderChart : function( self ) {

        var returned = this.prepData()
            values = returned[0],
            xVals = returned[1],
            yVals = returned[2]

        var minX = d3.min(xVals),
            maxX = d3.max(xVals),
            minY = d3.min(yVals),
            maxY = d3.max(yVals)

        var classSelector = '.scatter-plot'

        // A formatter for counts.
        var formatCount = d3.format(",.0f");

        d3.select(classSelector).select('svg').remove()

        var margin = {top: 50, right: 50, bottom: 50, left: 50},
            width = this.$el.width() - margin.left - margin.right,
            height = this.$el.height() - $('.exploration-heading').height() - margin.top - margin.bottom

        var y = d3.scale.linear().domain([minY, maxY]).range([ height, 0 ]),
            x = d3.scale.linear().domain([minX, maxX]).range([ 0, width ]),
            yAxis = d3.svg.axis().scale(y).orient("left").tickSize(1),
            xAxis = d3.svg.axis().scale(x).orient('bottom').tickSize(0)

        var svg = d3.select(classSelector).select('.vis-container').append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        //x axis
        d3.select(classSelector).selectAll('.x.axis')
            .attr('y', height)
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        svg.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis);

        //yticks
        d3.select(classSelector).selectAll('.y.axis')
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        svg.append("svg:g")
            .attr("class", "y axis")
            .attr("transform", "translate(0,0)")
            .style('fill-opacity', 0)
            .call(yAxis)
            .transition(500)
            .style('fill-opacity', 1)

        svg.selectAll("circle")
           .data(values)
          .enter()
           .append("circle")
           .attr("cx", function(d) {
                return x(d[0]);
           })
           .attr("cy", function(d) {
                return y(d[1]);
           })
           .attr("r", 5)
           .style('fill', 'steelblue')
           .style('fill-opacity', .4)

        var grays = svg.selectAll(".scatter-gray-y")
             .data(y.ticks(20), function(d) { return d })
           
        grays.enter().insert("line")
             .attr("x1", 0)
             .attr("x2", width)
             .attr("y1", y)
             .attr("y2", y)
             .attr("class", "scatter-gray-y")
             .style("stroke", "#bbb")

        grays.exit()
            .transition()
                .duration(500)
                .style('fill-opacity', 0)
                .remove()

        var xGrays = svg.selectAll(".scatter-gray-x")
             .data(x.ticks(20), function(d) { return d })
           
        xGrays.enter().insert("line")
             .attr("x1", x)
             .attr("x2", x)
             .attr("y1", 0)
             .attr("y2", height)
             .attr("class", "scatter-gray-x")
             .style("stroke", "#bbb")

        xGrays.exit()
            .transition()
                .duration(500)
                .style('fill-opacity', 0)
                .remove()

    },

    prepData : function(){

        var data = [],
            x = [],
            y = []

        _.each( this.model.data, function(obj){

            data.push([ obj["steps"], obj["calories_out"] ])
            x.push(obj["steps"])
            y.push(obj["calories_out"])

        })

        console.log([ data, x, y ])
        return [ data, x, y ]

    },

    changeDataSource : function( ev ) {
        var self = this

        $('.data-source').removeClass('data-source')
        $(ev.target).addClass('data-source')
        self.renderChart( self )

    },

    removeChart : function(){

        this.$el.remove()

    }

})