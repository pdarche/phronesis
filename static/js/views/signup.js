
var app = app || {}; 

app.LandingPage = Backbone.View.extend({

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

        "click #signup_button" : "move"

    },

    move : function(){

        $('.signup_container').addClass('transition-out')

    }

});