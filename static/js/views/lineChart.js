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

        var adj = $('.active-adj').html(),
            accent = accents[adj]

        var ddv = self.prepData(),
            data = ddv.data,
            dates = ddv.dates,
            vals = ddv.vals,
            mean = ddv.mean,
            median = ddv.median,
            mode = ddv.mode,
            sd = ddv.sd,
            contextData = 45


        var round2 = d3.format(".02r");

        var classSelector = '.line-chart'

        var drag = d3.behavior.drag()
            .origin(Object)
            .on("drag", dragmove);

        function dragmove(d) {
          console.log(d3.mouse(this)[1])
          console.log("d is", y(d))          
          d3.select(this)
              // .attr("transform", "translate(0," + (y(d) - mouse[1]) + ")" )
              // .attr("y", d.y = Math.max(radius, Math.min(height - radius, d3.event.y)));
        }        

        console.log("drag is", drag)

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
            .text(ddv.title);

        //x-axis labels
        vis.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", w)
            .attr("y", h - 10)
            .text(ddv.xAxis);

        //y-axis label
        vis.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("x", 0)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text(ddv.yAxis)
            .style('color', 'gray')


        var y = d3.scale.linear().domain([0, maxVal]).range([ h, 0 ]),
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
                .call(drag)


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

        meanLine.append("text")
            .text(function(){
                if ( $('.active-adj').html() === "healthy" ) {
                    return "+7% of developing CVD"
                } else {
                    return "4.6 tons of C02"
                }
            })
            .attr("id", "increase_text")
            .attr("x", w - 430)
            .attr("dy", -7)
            .style("font-size", 40)
            .style("fill", "red")
            .style('fill-opacity', .4)

        var contextLine = vis.append("svg:g")
              .data([contextData])
                .attr("id", "context")
                .attr("transform", "translate(0," + y(contextData) + ")")
                .on('mousedown', function(d){
                    console.log(d3.mouse(this))
                })

        contextLine.append("line")
             .attr("id", "mean_line")
             .attr("x1", 0 )
             .attr("x2", w)
             .attr("y1", 0)
             .attr("y1", 0)
             .style("stroke", "#444")
             .style("stroke-width", "1px")

        contextLine.append("text")
            .text(function(d){ return "goal"})
            .attr("id", "mean_text")
            .attr("x", -25)
            .attr("dy", 3)
            .style("font-size", 10)

        // contextLine.append("text")
        //     .text(function(d){ return "stdev: " + round2(sd)})
        //     .attr("id", "sd_text")
        //     .attr("x", 5)
        //     .attr("dy", 20)
        //     .style("font-size", 10)


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
              .style('stroke', accent)

        var circles = vis.selectAll(".value")
                .data(data)

        circles.enter().append("svg:circle")
            .attr("class", "value")
            .attr("fill", "none")
            .attr("stroke", accent)
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
            d3.select(this)
                .style('opacity', 1)
                .style('fill', accent)
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
            vals = [],
            dataType = this.getDataType(),
            x, y, title

        var sorted = this.model.data.sort(function(a,b) { return parseInt(a.created_at) - parseInt(b.created_at) } );

        _.each( sorted, function(obj){

            if ( dataType === "mins_very_active" ){
                var datum = { x: obj.created_at, y : obj[dataType] }
                vals.push(obj[dataType])
                x = "dates",
                y = "minutes",
                title = "Minutes Very Active"
            } else if ( dataType === "power" ) {
                var powerUsage = Math.floor(Math.random() * 2000) + 3000
                var datum = { x: obj.created_at, y : powerUsage }
                vals.push(powerUsage)
                x = "dates",
                y = "watts",
                title = "Average Watts Per Day"
            }

            data.push(datum)
            dates.push(obj.created_at)

        })

        var mean = j$(vals).mean(),
            median = j$(vals).median(),
            mode = j$(vals).mode(),
            sd = j$(vals).stdev()

        return { 
            data : data,
            dates : dates,
            vals : vals,
            mean : mean,
            median : median,
            mode : mode,
            sd : sd,
            xAxis : x,
            yAxis : y,
            title : title
        }

    },

    getDataType : function(){

        var activeAdj = $('.active-adj').html()

        var dataType

        switch(activeAdj){
            case "healthy":
                console.log("steps")
                dataType = "mins_very_active"
                break
            case "sustainable":
                dataType = "power" 
                console.log("power")
                break
            case "educated":
                dataType = "books"
                console.log("books")
                break
        }

        return dataType
    },

    getDataInfo : function(){

    },

    changeDataSource : function( ev ) {
        var self = this

        $('.data-source').removeClass('data-source')
        $(ev.target).addClass('data-source')
        self.renderChart( self )

    },

    addDataSource : function() {



    },

    removeDataSource : function() {



    },

    removeChart : function(){

        this.$el.remove()

    }





})