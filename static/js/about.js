// About Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations and interactions
    initSmoothScrolling(); // Initialize smooth scrolling
    initTimelineAnimations(); // Initialize timeline animations
    initTeamCardEffects(); // Initialize team card effects
});

// Smooth Scrolling
function initSmoothScrolling() {
    const scrollLinks = document.querySelectorAll('.scroll-to'); // Get all scroll links
    
    scrollLinks.forEach(link => { // Iterate over all scroll links
        link.addEventListener('click', function(e) { // Add click event listener to each scroll link
            e.preventDefault();
            const targetId = this.getAttribute('href'); // Get the target ID
            const targetElement = document.querySelector(targetId); // Get the target element
            
            if (targetElement) { // If the target element exists
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({ // Scroll to the target element
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Timeline Animations
function initTimelineAnimations() {
    const timelineItems = document.querySelectorAll('.timeline-item'); // Get all timeline items
    
    const observerOptions = { // Set the observer options
        threshold: 0.3,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => { // Create a new intersection observer
        entries.forEach((entry, index) => { // Iterate over all entries
            if (entry.isIntersecting) { // If the entry is intersecting
                setTimeout(() => { // Set a timeout to animate the entry
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 200); // Stagger animation
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions); // Observe the timeline items
    
    timelineItems.forEach(item => { // Iterate over all timeline items
        observer.observe(item); // Observe the timeline item
    });
}

// Team Card Hover Effects
function initTeamCardEffects() {
    const teamCards = document.querySelectorAll('.team-card'); // Get all team cards
    
    teamCards.forEach(card => { // Iterate over all team cards
        card.addEventListener('mouseenter', function() { // Add mouse enter event listener to each team card
            this.style.transform = 'translateY(-10px)'; // Move the team card up by 10px
        });
        
        card.addEventListener('mouseleave', function() { // Add mouse leave event listener to each team card
            this.style.transform = 'translateY(0)'; // Move the team card back to its original position
        });
    });
}

// Add loading animation for page elements
window.addEventListener('load', function() {
    document.body.classList.add('loaded'); // Add loaded class to the body
});

// Add CSS for loading animation
const style = document.createElement('style'); // Create a new style element
style.textContent = ` 
    body {
        opacity: 0;
        transition: opacity 0.5s ease;
    }
    
    body.loaded {
        opacity: 1;
    }
    
    .team-card {
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style); // Append the style element to the head