// ResaleX Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Загрузка...';
                submitBtn.disabled = true;
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });

    // Image preview functionality
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('previewImg');
                    const previewContainer = document.getElementById('imagePreview');
                    if (preview && previewContainer) {
                        preview.src = e.target.result;
                        previewContainer.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Alerts now stay visible until manually closed
    // Removed auto-hide functionality for better user experience

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .product-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => {
        observer.observe(card);
    });

    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Add search loading state
                const form = this.closest('form');
                if (form) {
                    form.classList.add('loading');
                    setTimeout(() => {
                        form.classList.remove('loading');
                    }, 1000);
                }
            }, 500);
        });
    }

    // Price formatting
    const priceElements = document.querySelectorAll('.price');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent);
        if (!isNaN(price)) {
            element.textContent = '$' + price.toFixed(2);
        }
    });

    // Add to cart animation
    const addToCartBtns = document.querySelectorAll('[data-action="add-to-cart"]');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add animation
            this.classList.add('pulse');
            setTimeout(() => {
                this.classList.remove('pulse');
            }, 1000);
            
            // Show success message
            showNotification('Товар добавлен в корзину!', 'success');
        });
    });

    // Wishlist functionality
    const wishlistBtns = document.querySelectorAll('[data-action="wishlist"]');
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const icon = this.querySelector('i');
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                this.classList.add('text-danger');
                showNotification('Добавлено в избранное!', 'success');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                this.classList.remove('text-danger');
                showNotification('Удалено из избранного', 'info');
            }
        });
    });

    // Quantity controls
    const quantityControls = document.querySelectorAll('.quantity-control');
    quantityControls.forEach(control => {
        const input = control.querySelector('input[type="number"]');
        const minusBtn = control.querySelector('.quantity-minus');
        const plusBtn = control.querySelector('.quantity-plus');
        
        if (minusBtn) {
            minusBtn.addEventListener('click', () => {
                const currentValue = parseInt(input.value) || 1;
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    updateTotal();
                }
            });
        }
        
        if (plusBtn) {
            plusBtn.addEventListener('click', () => {
                const currentValue = parseInt(input.value) || 1;
                input.value = currentValue + 1;
                updateTotal();
            });
        }
    });

    // Update total price
    function updateTotal() {
        const quantityInputs = document.querySelectorAll('input[name="quantity"]');
        const priceElements = document.querySelectorAll('.product-price');
        
        quantityInputs.forEach((input, index) => {
            const quantity = parseInt(input.value) || 1;
            const price = parseFloat(priceElements[index]?.textContent.replace('$', '')) || 0;
            const total = quantity * price;
            
            const totalElement = input.closest('.product-item')?.querySelector('.product-total');
            if (totalElement) {
                totalElement.textContent = '$' + total.toFixed(2);
            }
        });
    }

    // Filter functionality
    const filterBtns = document.querySelectorAll('[data-filter]');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Filter products
            const products = document.querySelectorAll('.product-card');
            products.forEach(product => {
                if (filter === 'all' || product.getAttribute('data-category') === filter) {
                    product.style.display = 'block';
                    product.classList.add('fade-in-up');
                } else {
                    product.style.display = 'none';
                }
            });
        });
    });

    // Sort functionality
    const sortSelect = document.querySelector('select[name="sort"]');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const productContainer = document.querySelector('.row.g-4');
            const products = Array.from(productContainer.querySelectorAll('.col-lg-3, .col-md-6'));
            
            products.sort((a, b) => {
                switch(sortBy) {
                    case 'price_low':
                        const priceA = parseFloat(a.querySelector('.text-primary')?.textContent.replace('$', '') || 0);
                        const priceB = parseFloat(b.querySelector('.text-primary')?.textContent.replace('$', '') || 0);
                        return priceA - priceB;
                    case 'price_high':
                        const priceA2 = parseFloat(a.querySelector('.text-primary')?.textContent.replace('$', '') || 0);
                        const priceB2 = parseFloat(b.querySelector('.text-primary')?.textContent.replace('$', '') || 0);
                        return priceB2 - priceA2;
                    case 'newest':
                        return 0; // Already sorted by newest
                    default:
                        return 0;
                }
            });
            
            // Re-append sorted products
            products.forEach(product => {
                productContainer.appendChild(product);
            });
        });
    }

    // Modal form validation
    const modalForms = document.querySelectorAll('.modal form');
    modalForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });

    // Real-time search suggestions
    const searchSuggestions = document.querySelector('.search-suggestions');
    if (searchSuggestions && searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length > 2) {
                // Simulate API call
                setTimeout(() => {
                    const suggestions = generateSuggestions(query);
                    displaySuggestions(suggestions);
                }, 300);
            } else {
                searchSuggestions.style.display = 'none';
            }
        });
    }

    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            const suggestions = document.querySelector('.search-suggestions');
            if (suggestions) {
                suggestions.style.display = 'none';
            }
        }
    });
});

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

function generateSuggestions(query) {
    // Mock suggestions - in real app, this would be an API call
    const suggestions = [
        'Air Jordan 1',
        'Nike Air Max',
        'Adidas Yeezy',
        'Supreme Box Logo',
        'Off-White',
        'Travis Scott',
        'Dior Jordan',
        'Fragment Design'
    ];
    
    return suggestions.filter(item => 
        item.toLowerCase().includes(query.toLowerCase())
    );
}

function displaySuggestions(suggestions) {
    const container = document.querySelector('.search-suggestions');
    if (!container) return;
    
    if (suggestions.length > 0) {
        container.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-item" data-suggestion="${suggestion}">${suggestion}</div>`
        ).join('');
        container.style.display = 'block';
        
        // Add click handlers
        container.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', function() {
                const searchInput = document.querySelector('input[name="search"]');
                if (searchInput) {
                    searchInput.value = this.getAttribute('data-suggestion');
                    searchInput.closest('form').submit();
                }
            });
        });
    } else {
        container.style.display = 'none';
    }
}

// Stripe payment integration
function initializeStripe() {
    if (typeof Stripe !== 'undefined') {
        const stripe = Stripe('pk_test_your_stripe_key'); // Replace with actual key
        const elements = stripe.elements();
        
        const cardElement = elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#424770',
                    '::placeholder': {
                        color: '#aab7c4',
                    },
                },
            },
        });
        
        cardElement.mount('#card-element');
        
        const form = document.getElementById('payment-form');
        if (form) {
            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                
                const {error} = await stripe.confirmCardPayment(
                    form.dataset.clientSecret,
                    {
                        payment_method: {
                            card: cardElement,
                        }
                    }
                );
                
                if (error) {
                    showNotification(error.message, 'error');
                } else {
                    showNotification('Платеж успешно обработан!', 'success');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 2000);
                }
            });
        }
    }
}

// Initialize Stripe when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeStripe);

// Export functions for global use
window.ResaleX = {
    showNotification,
    generateSuggestions,
    displaySuggestions
};
