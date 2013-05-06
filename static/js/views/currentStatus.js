var app = app || {};

app.CurrentStatusView = Backbone.View.extend({

    initialize : function() {

        console.log("model is", this.model.models[0].attributes)
        this.config = this.model.models[0].attributes

        var self = this
        console.log("the config is", self.config)

        if ( !($.isFunction(this.template)) ){
                
            $.when( 
                $.getJSON( self.config.data_url ),
                $.get('/static/js/templates/currentStatus.handlebars')
             )
             .done(
                function( data, tmpl ){
                    self.template = tmpl[0]
                    self.model = data[0]
                    var preppedData = self.prepData( self )
                    self.render( { "mean" : preppedData.mean, "heading" : self.config.heading }  )                      
                    self.renderChart( preppedData, self ) 
                }
             )
                    
            var accentClass = $('.active-adj').html() + "-accent"

        } else {

            console.log("gots the template")

        }

    },

    render : function( model ) {

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template( model ) );

    },

    events : {

        // "click .nav-adjective" : "toggleActions"

    },

    setModel : function() {

        var self = this 
        
        $.when( $.getJSON('v1/data/pdarche/body/physicalActivity?created_at__gte=1357020000&created_at__lte=1365375284') )
         .done( 
            function( data ){
                self.model = data
            }
         )

    },

    renderChart : function( data, self ) {

        var adj = $('.active-adj').html(),
            accent = accents[adj]

        var returnedData = data           
            data = returnedData.data
            values = returnedData.vals,
            dates = returnedData.dates,
            title = self.config.chart_title

        var round2 = d3.format(".02r");
        var classSelector = '.current-status'

        var margin = {top: 60, right: 30, bottom: 20, left: 50},
            w = self.$el.parent().width() - 250 - margin.left - margin.right,
            h = 80 //self.$el.height() - margin.top - margin.bottom

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
            .attr("x", 230)
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
            .attr('transform', 'translate(0, ' + 40 + ')')
            .call(xAxis);

        d3.select(classSelector).selectAll('.axis').selectAll('text')
            .attr("transform", "rotate(90)")
            .attr("x", 25)
            .attr("y", 0)
            .style('font-size', 12)
            .style('fill', 'gray')
            .attr("text-anchor", "start");

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

    prepData : function( self ){

        var data = [],
            dates = [],
            vals = [],
            dataType = self.getDataType(),
            x, y, title

        _.each( self.model, function(obj){

            var datum = { x: obj.created_at, y : obj[self.config.attr] }
                vals.push(obj[self.config.attr])
                x = "dates",
                y = "minutes",

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
                // console.log("steps")
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

})

Handlebars.registerHelper('round2', function(v){
    console.log("rounding this mother", v)
    return Math.round(v*10)/10
})