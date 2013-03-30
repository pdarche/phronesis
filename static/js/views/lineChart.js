var app = app || {};

app.LineChart = Backbone.View.extend({
    tagName : 'div',
    className : 'line-chart-container',
    id : undefined,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/lineChart.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.$el.attr( 'id', 'line_chart_' + $('.line-chart-container').length )
                var idSelector = '#' + self.$el.attr('id') 

                $(idSelector).draggable().resizable({
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

        console.log("the model Im rendering ", this.model)

    },

    events : {

        "click .destroy" : "removeChart"

    },

    renderChart : function() {

        console.log(this)

        var ddv = this.prepData(),
            data = ddv[0],
            dates = ddv[1],
            vals = ddv[2]

        var w = this.$el.width(),
            h = this.$el.height() - $('.destroy').height(),
            p = 20,
            idSelector = '#' + this.$el.attr('id')

        d3.select(idSelector).select('svg').remove()

        var minDate = new Date(d3.min(dates) * 1000),
            maxDate = new Date(d3.max(dates) * 1000),
            minVal = d3.min(vals)
            maxVal = d3.max(vals)

        var vis = d3.select(idSelector)
            .append("svg:svg")
            .attr("width", w + p)
            .attr("height", h + p)
                .append("svg:g")
                .attr("width", w)
                .attr("height", h)
                .attr("transform", "translate(" + 30 + ",0)")

        var y = d3.scale.linear().domain([minVal, maxVal]).range([ h - p, p ]),
            x = d3.time.scale().domain([minDate, maxDate]).range([ p, w - (2 * p) ]),
            yAxis = d3.svg.axis().scale(y).orient("left").tickSize(1)

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            // .ticks(d3.time.days, 1)
            .ticks(10)
            .tickFormat(d3.time.format('%b %d'))
            .tickSize(0)
            .tickPadding(8);

        d3.select(idSelector).selectAll('.x.axis')
            .attr('y', h + p)
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        vis.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + (h - p) + ')')
            .call(xAxis); 

        //yticks
        d3.select(idSelector).selectAll('.y.axis')
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

        var grays = vis.selectAll(".gray-line")
             .data(y.ticks(10), function(d) { return d })
           
        grays.enter().insert("line")
             .attr("x1", (2 * p) )
             .attr("x2", w)
             .attr("y1", y)
             .attr("y2", y)
             .attr("class", "gray-line")
             .style("stroke", "#bbb")

        grays.exit()
            .transition()
                .duration(500)
                .style('fill-opacity', 0)
                .remove()


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

        console.log(this.model.records)

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