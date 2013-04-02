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

        var ddv = self.prepData(),
            data = ddv[0],
            dates = ddv[1],
            vals = ddv[2]
            mean = ddv[3]
            median = ddv[4]
            mode = ddv[5]
            sd = ddv[6]

        var round2 = d3.format(".02r");

        var w =this.$el.width(),
            h = this.$el.height() - $('.destroy').height() - 80,
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
             .attr("x1", p )
             .attr("x2", w - (2 * p))
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
                .attr("transform", "translate(" + p + "," + y(mean) + ")")

        meanLine.append("line")
             .attr("id", "mean_line")
             .attr("x1", 0 )
             .attr("x2", w - (3 * p))
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

    prepData : function( selected ){

        var data = [],
            dates = [],
            vals = [],
            selected = $('.data-source').attr('id')

            console.log("the selected attribute is", selected)

        _.each( this.model.records, function(obj){

            var datum = { x: obj.created_at, y : obj[selected] }

            data.push(datum)
            dates.push(obj.created_at)
            vals.push(obj[selected])

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