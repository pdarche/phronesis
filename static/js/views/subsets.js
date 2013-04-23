var app = app || {};

app.Subsets = Backbone.View.extend({
    tagName : 'div',
    className : 'subsets',

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/subsets.handlebars', function(tmpl){
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

        var returnedData = this.prepData(),            
            data = returnedData.data
            values = returnedData.vals,
            dates = returnedData.dates,
            title = returnedData.title

        var round2 = d3.format(".02r");

        var classSelector = '.subsets'

        var margin = {top: 60, right: 30, bottom: 20, left: 50},
            w = this.$el.width() - margin.left - margin.right,
            h = this.$el.height() - 75 - margin.top - margin.bottom

        d3.select(classSelector).select('svg').remove()

        var minDate = new Date(d3.min(dates) * 1000),
            maxDate = new Date(d3.max(dates) * 1000)

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
            .attr("y", 20)
            .text(title);

        var x = d3.time.scale().domain([minDate, maxDate]).range([ 0, w ])

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .ticks(10)
            .tickFormat(d3.time.format('%b %d'))
            .tickSize(0)
            .tickPadding(5);

        vis.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + ( h - 5 ) + ')')
            .call(xAxis);

        d3.select(classSelector).selectAll('.axis').selectAll('text')
            .attr("transform", "rotate(90)")
            .attr("x", 25)
            .attr("y", 0)
            .style('font-size', 12)
            .style('fill', 'gray')
            .attr("text-anchor", "start");

        console.log("the vis is ", vis)

        var circles = vis.selectAll(".value")
                .data(data)

        circles.enter().append("svg:circle")
            .attr("class", "value")
            .attr("stroke", accent)
            .transition()
                .duration(500)
                .attr("cx", function(d) {
                    var date = new Date(d.x * 1000)
                    return x(date)
                })
                .attr("cy", function(d) { 
                    var yPos
                    d.y >= 10000 ? yPos = -10 : yPos = 30
                    return yPos; 
                })
                .attr("r", 4)
                // .attr("fill", accent)
                .attr("fill", function(d){
                    var stroke
                    d.y >= 10000 ? stroke = "green" : stroke = "red"
                    return stroke;   
                })
            // .style("opacity", 0)

        // circles.on('mouseover',function(obj){
        //     console.log(obj)
        //     d3.select(this)
        //         .style('opacity', 1)
        //         .style('fill', accent)
        // })
        // .on('mouseout', function(){
        //     d3.select(this)
        //         .style('opacity', 0)
        // })

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

        _.each( this.model.data, function(obj){

            if ( dataType === "steps" ){
                var datum = { x: obj.created_at, y : obj[dataType] }
                vals.push(obj[dataType])
                x = "dates",
                y = "minutes",
                title = "Over or Under 10,000 Steps"
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
                dataType = "steps"
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