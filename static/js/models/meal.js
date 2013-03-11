 Meal = Backbone.Model.extend({
        defaults: {
            name: '',
            age: 0
        },
        initialize: function(){            
            this.on("change:name", function(model){
                var name = model.get("name"); // 'Stewie Griffin'
                alert("Changed my name to " + name );
            });
        }
});