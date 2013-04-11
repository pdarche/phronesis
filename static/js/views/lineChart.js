var app = app || {};

app.LineChart = Backbone.View.extend({
    tagName : 'div',
    className : 'line-chart',

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/lineChart.handlebars', function(tmpl){
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

        var ddv = self.prepData(),
            data = ddv[0],
            dates = ddv[1],
            vals = ddv[2]
            mean = ddv[3]
            median = ddv[4]
            mode = ddv[5]
            sd = ddv[6]

        var round2 = d3.format(".02r");

        var classSelector = '.line-chart'

        var margin = {top: 60, right: 30, bottom: 20, left: 50},
            w = this.$el.width() - margin.left - margin.right,
            h = this.$el.height() - 75 - margin.top - margin.bottom

        d3.select(classSelector).select('svg').remove()

        var minDate = new Date(d3.min(dates) * 1000),
            maxDate = new Date(d3.max(dates) * 1000),
            minVal = d3.min(vals)
            maxVal = d3.max(vals)

        var vis = d3.select(classSelector).select('.vis-container')
            .append("svg:svg")
            // .attr("transform", "translate(0," + 20 + ")")
            .attr("width", w + margin.left + margin.right)
            .attr("height", h + margin.top + margin.bottom + 50)
                .append("svg:g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        //title
        d3.select(classSelector).select('.vis-container').select('svg')
            .append("text")
            .attr("class", "title")
            .attr("text-anchor", "middle")
            .attr("x", 270)
            .attr("y", 40)
            .text("Steps Taken");

        //x-axis labels
        vis.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", w)
            .attr("y", h - 10)
            .text("Date");

        //y-axis label
        vis.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("x", 0)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text("Steps");        


        var y = d3.scale.linear().domain([minVal, maxVal]).range([ h, 0 ]),
            x = d3.time.scale().domain([minDate, maxDate]).range([ 0, w ]),
            yAxis = d3.svg.axis().scale(y).orient("left").tickSize(1)

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .ticks(6)
            .tickFormat(d3.time.format('%b %d'))
            .tickSize(0)
            .tickPadding(5);

        d3.select(classSelector).selectAll('.x.axis')
            .attr('y', h)
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        vis.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + h + ')')
            .call(xAxis);

        //yticks
        d3.select(classSelector).selectAll('.y.axis')
            .transition(500)
            .style("fill-opacity", 0)
            .remove()

        vis.append("svg:g")
            .attr("class", "y axis")
            .attr("transform", "translate(0,0)")
            .style('fill-opacity', 0)
            .call(yAxis)
            .transition(500)
            .style('fill-opacity', 1)

        var grays = vis.selectAll(".gray-line")
             .data(y.ticks(10), function(d) { return d })
           
        grays.enter().insert("line")
             .attr("x1", 0)
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

        var meanLine = vis.append("svg:g")
              .data([mean])
                .attr("id", "mean")
                .attr("transform", "translate(0," + y(mean) + ")")

        meanLine.append("line")
             .attr("id", "mean_line")
             .attr("x1", 0 )
             .attr("x2", w)
             .attr("y1", 0)
             .attr("y1", 0)
             .style("stroke", "444")
             .style("stroke-width", "2px")

        meanLine.append("text")
            .text(function(d){ return "mean: " + round2(d)})
            .attr("id", "mean_text")
            .attr("x", 5)
            .attr("dy", 10)
            .style("font-size", 10)

        meanLine.append("text")
            .text(function(d){ return "stdev: " + round2(sd)})
            .attr("id", "sd_text")
            .attr("x", 5)
            .attr("dy", 20)
            .style("font-size", 10)

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
              .style('stroke-width', 2)

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
            .style("opacity", 0)

        circles.on('mouseover',function(obj){
            console.log(obj)
            d3.select(this)
                .style('opacity', 1)
                .style('fill', 'steelblue')
        })
        .on('mouseout', function(){
            d3.select(this)
                .style('opacity', 0)
        })

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

    prepData : function( selected ){

        var data = [],
            dates = [],
            vals = []

        _.each( this.model.data, function(obj){

            var datum = { x: obj.created_at, y : obj["steps"] }

            data.push(datum)
            dates.push(obj.created_at)
            vals.push(obj["steps"])

        })

        var mean = j$(vals).mean(),
            median = j$(vals).median(),
            mode = j$(vals).mode(),
            sd = j$(vals).stdev()

        return [ data, dates, vals, mean, median, mode, sd ]

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

    addDataSource : function() {



    },

    removeDataSource : function() {



    },

    removeChart : function(){

        this.$el.remove()

    }

})