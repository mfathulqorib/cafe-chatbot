function priceFormatter() {
    return {
        display: '',
        init() {
            const el = document.getElementById('price');
            const raw = el.value.replace(/\D/g, '');
            this.display = raw ? new Intl.NumberFormat('id-ID').format(raw) : '';
        },
        get numeric() {
            // Remove all non-digit characters
            return this.display.replace(/\D/g, '');
        },
        format() {
            let number = this.numeric;
            if (number) {
                this.display = new Intl.NumberFormat('id-ID').format(number);
            }
        },
        removeFormat() {
            this.display = this.numeric;
        },
        onlyAllowNumericInput(event) {
            const allowed = ['0','1','2','3','4','5','6','7','8','9','.'];
            if (!allowed.includes(event.key)) {
                event.preventDefault();
            }
        }
    }
}