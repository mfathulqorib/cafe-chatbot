// transaction-form.js
function transactionForm(menuItems, formData = {}) {
    const inputMenuItem = document.getElementById('menu-item')
    const items = []
    let index = 0;

    while (`id_${index}` in formData) {
    items.push({
        id: formData[`id_${index}`],
        name: formData[`name_${index}`],
        price: parseInt(formData[`price_${index}`], 10),
        qty: parseInt(formData[`quantity_${index}`], 10)
    });
    index++;
    }
      
    return {
      selectedItemId: '',
      selectedQty: 1,
      items: items,
      showWarning: false,
      warningMessage: '',
      
      // Format currency in Indonesian Rupiah format
      formatCurrency(amount) {
        return 'Rp ' + new Intl.NumberFormat('id-ID').format(amount);
      },
      
      // Calculate total amount from all items
      calculateTotal() {
        return this.items.reduce((sum, item) => sum + (item.price * item.qty), 0);
      },
      
      // Add an item to the transaction
      addItem() {
        if (!this.selectedItemId) {
          this.warningMessage = "Select menu item!";
          this.showWarning = true;
          inputMenuItem.focus()
          return;
        }
  
        this.showWarning = false;
  
        const existing = this.items.find(i => i.id === this.selectedItemId);

        if (existing) {
          existing.qty += parseInt(this.selectedQty);
        } else {
          const selectedItem = menuItems[this.selectedItemId];
          this.items.push({
            id: this.selectedItemId,
            name: selectedItem.name,
            price: selectedItem.price,
            qty: parseInt(this.selectedQty),
          });
        }
  
        this.selectedItemId = '';
        this.selectedQty = 1;
      },
      
      // Increase quantity of an item
      incrementQty(index) {
        this.items[index].qty += 1;
      },
      
      // Decrease quantity of an item
      decrementQty(index) {
        if (this.items[index].qty > 1) {
          this.items[index].qty -= 1;
        }
      },
      
      // Remove an item from the transaction
      removeItem(index) {
        this.items.splice(index, 1);
      },

      phoneNumberValidation(event) {
        this.showWarning = false;

        const el = document.getElementById("customer_phone")
        const value = el.value
        const allowed = ['0','1','2','3','4','5','6','7','8','9','.'];
        if (!allowed.includes(event.key) | value.length > 12) {
            event.preventDefault();
        }
        
        if (value.length > 12) {
          this.warningMessage = "Maximum 13 digits for phone number!";
          this.showWarning = true;
        } 
    }
    };
  }