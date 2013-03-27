var app = app || {};

app.QueryView = Backbone.View.extend({
    
    startDate : undefined,
    endDate : undefined,

    initialize: function(){

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/queryContainer.handlebars', function(tmpl){
                self.template = tmpl
                self.render( tmpl )

                $( "#range_container" ).slider({
                    range : true,
                    min : 0,
                    max : 100,
                    values : [75,100],
                    slide: function( event, ui ) {
                        self.startDate = ui.values[0]
                        self.endDate = ui.values[1]
                    }
                });

            })

        } else {

            console.log("gots the template")

        }

    },

    render: function( tmpl ){

        $('body').append('<div id="chart_container"></div>')

        var source = $(tmpl).html()
        var template = Handlebars.compile( source )
        $('body').append( template )

        var pad = 80,
            w = window.innerWidth - (2*pad),
            h = window.innerHeight - (2*pad)

        var linedata = function( w, numLines ){
            
            var sep = w/numLines,
                data = []

            for ( var i = 1; i < numLines; i++ ) {
                data.push( (sep * i) )
            } 

            return data
        }

        var vis = d3.select('#chart_container')
            .append('svg')
            .attr('width', window.innerWidth)
            .attr('height', window.innerHeight)
            .append('svg:g')
                .attr('transform', 'translate(' + (w/2 + pad) + ',' + pad + ')')

        vis.append('rect').attr('width', w/2).attr('height', h)

        vis.selectAll('line.xGrid')
            .data(linedata(w/2,30))
          .enter().append('line')
            .attr('class', 'xGrid')
            .attr('x1', function(d) { return d })
            .attr('x2', function(d) { return d })
            .attr('y1', 0)
            .attr('y2', h)

        vis.selectAll('line.yGrid')
            .data(linedata(h,30))
          .enter().append('line')
            .attr('class', 'yGrid')
            .attr('y1', function(d) { return d })
            .attr('y2', function(d) { return d })
            .attr('x1', 0)
            .attr('x2', w/2)

        vis.append('text').text('Drag Records Here')
            .attr('font-size', '50px')
            .attr('x', function(){
                var offset = w/4 - d3.select('text').node().getComputedTextLength()/2
                return offset
            })
            .attr('y', h/2)
            .style('fill', 'gray')
            .on('mouseover', function(){
                d3.select('rect').style('stroke', 'white')
            })
            .on('mouseout', function(){
                d3.select('rect').style('stroke', 'grey')
            })

        // d3.select('body').insert('div')
        //     .style('fixed','top')
        //     .style('height','100px')
        //     .style('background-color', 'rgba(255,255,255,.6)')
        //     .style('border-bottom', '1px solid white')
        //     .style('box-shadow', '0px 2px 10px gray')

    },
    
    events : {

        "click .category" : "chooseCategory",
        "change select" : "getRecords"

    },

    chooseCategory : function(ev){

        $('.chosen').removeClass('chosen')
        $(ev.target).addClass('chosen')
        //get start date from records
        //get min date from records
        //set start and end date in slider

    },

    timeRange : function(){

    },

    getRecords : function(){

        var category = $('.chosen').attr('id'),
            limit = $('#limit input').val(),
            order_by = $('#ordering option:selected').val(),
            dateValues = $('.ui-slider-range').value

        if ( category === undefined ) {
            console.log("no category selected")
            return 
        }

        var url = '/v1/data/pdarche/body/' + category + '?' + this.checkDefined('order_by', order_by)
            url += this.checkDefined('limit', limit, "&") 

        $.getJSON(url, function(data){
            console.log(data)
        })

    },

    checkDefined : function(key,val,amp) {

        amp === undefined ? amp = "" : null

        if ( val === undefined ) {
            return ""
        } else {
            return amp+key + '=' + val
        }

    }

});
