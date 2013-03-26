
var app = app || {}; 

app.LandingPage = Backbone.View.extend({
    tagName : 'div',

    initialize: function(){
        
        this.render()

    },

    render : function() {

        var w = window.innerWidth/4,
            d = [ w - w/2,  (w * 2) - w/2 , (w*3) - w/2, (w*4) - w/2 ]

        d3.select('body').style('position', 'relative').style('height', 900)

        var vis = d3.select('body')
            .append('svg')
            .attr('width', function(){ return window.innerWidth})
            .attr('height', function(){ return window.innerHeight})

        var circles = d3.select('svg').selectAll('.test')
          .data(d)
        .enter().append('svg:circle')
          .transition()
          .attr('class', 'test')
          .attr('cy', function() { return window.innerHeight/2})
          .attr('cx', function(d){ return d })
          .attr('r', 100)
          .attr('fill', 'green')
          .attr('opacity', .4)

        d3.selectAll('circle').on('click', function(){
            
            var self = this

            var min = -500,
                max = 1500

            d3.selectAll('circle')
              .transition()
              .attr('cx', function() {
                if ( this === self ) {
                    return window.innerWidth/2
                } else {
                    return Math.floor(Math.random() * (max - min + 1)) + min;
                }
              })
              .attr('cy', function() {
                if ( this === self ) {
                    return window.innerHeight/2
                } else {
                    return Math.floor(Math.random() * (max - min + 1)) + min;
                }
              })

        })

    }

})