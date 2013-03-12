var mealView = '\
                <h1 class="eaten-date">{{date}}</h1>
                <div class="meal-container">
                    <div class="image-container"> 
                        <img src="{{img_url}}"/>
                    </div>
                    <div class="meal-info-container">
                        <h2>{{meal_item_name}}</h2>
                        <h3>{{#formatTime}}{{flkr_dates.taken}}{{/formatTime}}</h3>
                    </div>
                </div>