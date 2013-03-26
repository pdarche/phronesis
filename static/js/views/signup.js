
var app = app || {}; 

app.Login = Backbone.View.extend({

    initialize: function(){
        
        if ( !($.isFunction(this.template)) ){

            var self = this;    
            $.get('/static/js/templates/landingpage.handlebars', function(tmpl){
                self.template = tmpl;
                self.render();
            })

        } else {

            console.log("gots the template");

        }

    },

    render: function(){

        var source = $(this.template).html();
        var template = Handlebars.compile(source);
        this.$el.html( template );

        return this;

    },

    events : {

        "click #signup_button" : "login",

    },

    login : function() {

        this.accept()

    },

    accept : function() {

        var self = this

        d3.select('.signup_container')
            // .style('box-shadow', '0px 2px 10px lightgreen')
            .style('border', '2px solid lightgreen')
          .transition()
            .call(setTimeout(self.move, 500))

    },

    reject : function() {

        d3.select('.signup_container')
            .style('box-shadow', '0px 2px 10px lightred')
            .style('border', '1px solid lightred')
          .transition() 

    },

    move : function(){

        d3.select('.signup_container')
            .transition()
                .duration(250)
            .style('margin', '-100px auto')
            .remove()
            .call( setTimeout(function(){
                window.location.hash = 'query'
            }, 500))

    }

});