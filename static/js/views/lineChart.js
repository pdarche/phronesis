var app = app || {};

app.LineChart = Backbone.View.extend({
    tagName : 'div',
    className : 'line-chart-container',
    id : 'line_chart_' + $('.line-chart-container').length,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/lineChart.handlebars', function(tmpl){
                self.template = tmpl
                self.render()

                $('.line-chart-container').draggable().resizable({
                    stop : function() {
                        self.renderChart()
                    }
                })

                self.renderChart()

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template(this.model) )

    },

    events : {

        "click .destroy" : "removeChart"

    },

    renderChart : function() {

        var ddv = this.prepData(),
            data = ddv[0],
            dates = ddv[1],
            vals = ddv[2]

        d3.select('svg').remove()

        var w = this.$el.width(),
            h = this.$el.height() - $('.destroy').height(),
            p = 20,
            idSelector = '#' + this.id

        var minDate = new Date(d3.min(dates) * 1000),
            maxDate = new Date(d3.max(dates) * 1000),
            minVal = d3.min(vals)
            maxVal = d3.max(vals)

        var vis = d3.select(idSelector)
            .append("svg:svg")
            .attr("width", w)
            .attr("height", h)
            .append("svg:g")
            .attr("transform", "translate(" + 30 + ",0)")

        var y = d3.scale.linear().domain([minVal, maxVal]).range([ h - p, p ]),
            x = d3.time.scale().domain([minDate, maxDate]).range([ (3 * p), w - (2 * p) ]),
            yAxis = d3.svg.axis().scale(y).orient("left").tickSize(1)

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            // .ticks(d3.time.days, 1)
            .ticks(20)
            .tickFormat(d3.time.format('%a %d'))
            .tickSize(0)
            .tickPadding(8);

        d3.selectAll('.x.axis')
            .attr('y', h + p)
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        vis.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + (h - p) + ')')
            .call(xAxis);            

        //yticks
        d3.selectAll('.y.axis')
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        vis.append("svg:g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + p + ",0)")
            .style('fill-opacity', 0)
            .call(yAxis)
            .transition(500)
            .style('fill-opacity', 1)

        var path = vis.append("g").selectAll("path.line")
            .data([data])

        path.enter().append("svg:path")
          .attr("class", "line")
          .attr("d", d3.svg.line().x(0).y(0) )
          .transition()
              .attr("d", d3.svg.line()
                  .interpolate("cardinal")
                  .x(function(d) {
                    var date = new Date(d.x * 1000)
                    return x(date) 
                  })
                  .y(function(d) { return y(d.y) })
              )

        var circles = vis.selectAll(".value")
                .data(data)

        circles.enter().append("svg:circle")
            .attr("class", "value")
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .transition()
                .duration(500)
                .attr("cx", function(d) {
                    var date = new Date(d.x * 1000)
                    return x(date)
                })
                .attr("cy", function(d) { return y(d.y); })
                .attr("r", 4)

        circles.exit()
            .transition()
                .duration(500)
                .attr("cx", function(d) {
                    var date = new Date(d.x * 1000)
                    return x(date) 
                })
                .attr("cy", function(d) { return y(d.y); })
            .remove();

    },

    prepData : function(){

        var data = [],
            dates = [],
            vals = []

        _.each( this.model.records, function(obj){
            
            var datum = { x: obj.created_at, y : obj.steps }

            data.push(datum)
            dates.push(obj.created_at)
            vals.push(obj.steps)

        })

        return [ data, dates, vals ]

    },

    removeChart : function(){

        this.$el.remove()

    }

})