import os

# Define the templates to be created
TEMPLATES = {
    "workers/worker_list.html": """{% extends 'base.html' %}
{% block content %}
<div>
    <div>
        <h1>Available Workers</h1>
        <form method="get">
            <input type="text" name="service" placeholder="Search services...">
            <button type="submit">Search</button>
        </form>
    </div>

    <div>
        {% for worker in workers %}
            <article>
                {% if worker.profile_picture %}
                    <img src="{{ worker.profile_picture.url }}" alt="{{ worker.user.username }}">
                {% endif %}
                <div>
                    <h2>{{ worker.user.get_full_name }}</h2>
                    <p>Services: {{ worker.services_offered }}</p>
                    <p>Rate: ${{ worker.hourly_rate }}/hour</p>
                    {% if worker.rating %}
                        <p>Rating: {{ worker.rating }}/5</p>
                    {% endif %}
                    <a href="{% url 'workers:worker_detail' worker.pk %}">View Profile</a>
                </div>
            </article>
        {% empty %}
            <p>No workers found matching your criteria.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}
""",
    "workers/worker_detail.html": """{% extends 'base.html' %}
{% block content %}
<article>
    <header>
        {% if worker.profile_picture %}
            <img src="{{ worker.profile_picture.url }}" alt="{{ worker.user.username }}">
        {% endif %}
        <h1>{{ worker.user.get_full_name }}</h1>
    </header>

    <section>
        <h2>Services Offered</h2>
        <p>{{ worker.services_offered }}</p>
        <p>Rate: ${{ worker.hourly_rate }}/hour</p>
        {% if worker.rating %}
            <p>Rating: {{ worker.rating }}/5</p>
        {% endif %}
    </section>

    {% if user.is_authenticated %}
        <section>
            <h2>Book This Worker</h2>
            <form method="post" action="{% url 'workers:create_booking' worker.pk %}">
                {% csrf_token %}
                {{ booking_form.as_p }}
                <button type="submit">Book Now</button>
            </form>
        </section>
    {% endif %}

    <section>
        <h2>Reviews</h2>
        {% for review in reviews %}
            <article>
                <p>Rating: {{ review.rating }}/5</p>
                <p>{{ review.comment }}</p>
                <p>By {{ review.customer.username }} on {{ review.created_at|date }}</p>
            </article>
        {% empty %}
            <p>No reviews yet.</p>
        {% endfor %}
    </section>
</article>
{% endblock %}
""",
    "workers/worker_dashboard.html": """{% extends 'base.html' %}
{% block content %}
<div>
    <h1>Worker Dashboard</h1>
    
    <section>
        <h2>Upcoming Bookings</h2>
        {% for booking in upcoming_bookings %}
            <article>
                <p>Customer: {{ booking.customer.username }}</p>
                <p>Date: {{ booking.scheduled_time }}</p>
                <p>Service: {{ booking.service_description }}</p>
                <p>Status: {{ booking.get_status_display }}</p>
            </article>
        {% empty %}
            <p>No upcoming bookings.</p>
        {% endfor %}
    </section>

    <section>
        <h2>Recent Reviews</h2>
        {% for review in recent_reviews %}
            <article>
                <p>Rating: {{ review.rating }}/5</p>
                <p>{{ review.comment }}</p>
                <p>By {{ review.customer.username }} on {{ review.created_at|date }}</p>
            </article>
        {% empty %}
            <p>No reviews yet.</p>
        {% endfor %}
    </section>
</div>
{% endblock %}
""",
    "bookings/booking_history.html": """{% extends 'base.html' %}
{% block content %}
<div>
    <h1>Booking History</h1>
    {% for booking in bookings %}
        <article>
            {% if user.worker_profile %}
                <p>Customer: {{ booking.customer.username }}</p>
            {% else %}
                <p>Worker: {{ booking.worker.user.username }}</p>
            {% endif %}
            <p>Date: {{ booking.scheduled_time }}</p>
            <p>Service: {{ booking.service_description }}</p>
            <p>Status: {{ booking.get_status_display }}</p>
            <p>Total Cost: ${{ booking.total_cost }}</p>
            {% if booking.can_cancel %}
                <form method="post" action="{% url 'workers:cancel_booking' booking.id %}">
                    {% csrf_token %}
                    <button type="submit">Cancel Booking</button>
                </form>
            {% endif %}
        </article>
    {% empty %}
        <p>No bookings found.</p>
    {% endfor %}
</div>
{% endblock %}
""",
    "workers/worker_calendar.html": """{% extends 'base.html' %}
{% block content %}
<div>
    <h1>Work Calendar</h1>
    <div>
        {% for booking in bookings %}
            <article>
                <p>Date: {{ booking.scheduled_time }}</p>
                <p>Customer: {{ booking.customer.username }}</p>
                <p>Service: {{ booking.service_description }}</p>
                <p>Duration: {{ booking.duration_hours }} hours</p>
                <p>Status: {{ booking.get_status_display }}</p>
            </article>
        {% empty %}
            <p>No scheduled bookings.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}
""",
    "workers/review_form.html": """{% extends 'base.html' %}
{% block content %}
<div>
    <h1>Write a Review</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit Review</button>
    </form>
</div>
{% endblock %}
""",
}

# Define the base templates folder
BASE_TEMPLATES_FOLDER = os.path.join( "templates","services")

# Create and write templates
for path, content in TEMPLATES.items():
    full_path = os.path.join(BASE_TEMPLATES_FOLDER, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Create directories if not exists
    with open(full_path, "w") as file:
        file.write(content)

print("Templates generated successfully!")
