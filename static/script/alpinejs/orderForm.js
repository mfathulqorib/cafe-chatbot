// transaction-form.js
function orderForm(menuItems, order_items = []) {
    // Constants
    const PHONE_NUMBER_MAX_LENGTH = 12;
    const ALLOWED_PHONE_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'];
    
    // DOM Elements
    const inputMenuItem = document.getElementById('menu-item');
    
    // Initialize items from form data
    const items = order_items;
      
    return {
        // State
        selectedItemId: '',
        selectedQty: 1,
        items: items,
        showWarning: false,
        warningMessage: '',
        
        // Utility Methods
        formatCurrency(amount) {
            if (typeof amount !== 'number') {
                console.warn('formatCurrency received non-number input:', amount);
                return 'Rp 0';
            }
            return 'Rp ' + new Intl.NumberFormat('id-ID').format(amount);
        },
        
        calculateTotal() {
            return this.items.reduce((sum, item) => {
                if (!item.price || !item.qty) {
                    console.warn('Invalid item data:', item);
                    return sum;
                }
                return sum + (item.price * item.qty);
            }, 0);
        },
        
        // Item Management Methods
        addItem() {
            if (!this.selectedItemId) {
                this.setWarning("Select menu item!");
                inputMenuItem.focus();
                return;
            }

            this.showWarning = false;
            const existingItem = this.items.find(i => i.id === this.selectedItemId);

            if (existingItem) {
                existingItem.qty += parseInt(this.selectedQty);
            } else {
                const selectedItem = menuItems[this.selectedItemId];
                if (!selectedItem) {
                    this.setWarning("Selected item not found!");
                    return;
                }
                
                this.items.push({
                    id: this.selectedItemId,
                    name: selectedItem.name,
                    price: selectedItem.price,
                    qty: parseInt(this.selectedQty),
                });
            }
            document.getElementById('selected-items').classList.remove('hidden');
  
            this.resetSelection();
        },
        
        incrementQty(index) {
            if (this.items[index]) {
                this.items[index].qty += 1;
            }
        },
        
        decrementQty(index) {
            if (this.items[index] && this.items[index].qty > 1) {
                this.items[index].qty -= 1;
            }
        },
        
        removeItem(index) {
            if (this.items[index]) {
                this.items.splice(index, 1);
            }
        },

        // Helper Methods
        setWarning(message) {
            // Show warning message by removing hidden class
            document.getElementById('warning-message').classList.remove('hidden');
            this.warningMessage = message;
            this.showWarning = true;
        },

        resetSelection() {
            this.selectedItemId = '';
            this.selectedQty = 1;
        },

        // Validation Methods
        phoneNumberValidation(event) {
            this.showWarning = false;
            const el = document.getElementById("customer_phone");
            const value = el.value;
            
            if (!ALLOWED_PHONE_CHARS.includes(event.key) || value.length > PHONE_NUMBER_MAX_LENGTH) {
                event.preventDefault();
            }
            
            if (value.length > PHONE_NUMBER_MAX_LENGTH) {
                this.setWarning("Maximum 13 digits for phone number!");
            }
        }
    };
}