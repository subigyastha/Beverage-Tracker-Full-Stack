// dynamic_subcategories.js
document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.querySelector('select[name="category"]');
    const subcategorySelect = document.querySelector('select[name="subcategory"]');
    const customCategoryInput = document.querySelector('input[name="custom_category"]');
    const customSubcategoryInput = document.querySelector('input[name="custom_subcategory"]');

    if (categorySelect && subcategorySelect) {
        const subcategories = {
            'water': [
                ['plain_water', 'Plain Water'],
                ['infused_water', 'Infused Water (Lemon, Cucumber, Mint, Ginger)'],
                ['coconut_water', 'Coconut Water'],
                ['electrolyte_water', 'Electrolyte-Infused Water'],
                ['oral_rehydration', 'Oral Rehydration Solutions']
            ],
            'coffee': [
                ['black_coffee', 'Black Coffee'],
                ['espresso', 'Espresso'],
                ['americano', 'Americano'],
                ['cold_brew', 'Cold Brew'],
                ['latte_dairy', 'Latte (Dairy-Based)'],
                ['latte_plant', 'Latte (Plant-Based)'],
                ['cappuccino', 'Cappuccino'],
                ['mocha', 'Mocha']
            ],
            'tea': [
                ['green_tea', 'Green Tea'],
                ['black_tea', 'Black Tea'],
                ['white_tea', 'White Tea'],
                ['oolong_tea', 'Oolong Tea'],
                ['herbal_tea', 'Herbal Tea [Peppermint, Chamomile, Ginger, Fennel, Licorice Root]'],
                ['matcha', 'Matcha'],
                ['yerba_mate', 'Yerba Mate']
            ],
            'juice_smoothie': [
                ['fresh_fruit_juice', 'Fresh Fruit Juice [Apple, Orange, Pomegranate, etc.]'],
                ['vegetable_juice', 'Vegetable Juice [Carrot, Beet, Celery, etc.]'],
                ['fruit_smoothie', 'Blended Smoothies [Fruit-Based]'],
                ['vegetable_smoothie', 'Blended Smoothies [Vegetable-Based]']
            ],
            'dairy': [
                ['whole_milk', 'Whole Milk'],
                ['low_fat_milk', 'Low-Fat Milk'],
                ['skim_milk', 'Skim Milk'],
                ['lactose_free_milk', 'Lactose-Free Milk'],
                ['kefir', 'Kefir'],
                ['buttermilk', 'Buttermilk']
            ],
            'plant_milk': [
                ['almond_milk_unsweetened', 'Almond Milk [Unsweetened]'],
                ['almond_milk_sweetened', 'Almond Milk [Sweetened]'],
                ['oat_milk_unsweetened', 'Oat Milk [Unsweetened]'],
                ['oat_milk_sweetened', 'Oat Milk [Sweetened]'],
                ['soy_milk', 'Soy Milk'],
                ['coconut_milk', 'Coconut Milk'],
                ['rice_milk', 'Rice Milk'],
                ['hemp_milk', 'Hemp Milk']
            ],
            'fermented': [
                ['kombucha', 'Kombucha'],
                ['lassi', 'Lassi'],
                ['yakult', 'Yakult'],
                ['kvass', 'Kvass']
            ],
            'carbonated': [
                ['regular_soda', 'Regular Soda'],
                ['diet_soda', 'Diet Soda'],
                ['sparkling_water', 'Sparkling Water'],
                ['energy_drinks', 'Energy Drinks'],
                ['sports_drinks', 'Sports Drinks [Gatorade, Powerade]']
            ],
            'alcohol': [
                ['beer', 'Beer'],
                ['wine', 'Wine'],
                ['cider', 'Cider'],
                ['cocktails', 'Cocktails'],
                ['liquor', 'Liquor [Vodka, Whiskey, Gin, Tequila]']
            ],
            'other': [
                ['custom', 'Custom Entry']
            ]
        };

        function updateSubcategories() {
            const category = categorySelect.value;
            console.log('Updating subcategories for category:', category);

            // Use window.initialSubcategory if set, otherwise fall back to select value
            const currentSubcategory = window.initialSubcategory || subcategorySelect.value || '';
            console.log('Current subcategory before update:', currentSubcategory);

            subcategorySelect.innerHTML = '<option value="">---------</option>';
            console.log('Subcategories for', category, ':', subcategories[category]);

            if (category === 'other') {
                subcategorySelect.disabled = true;
                customCategoryInput.disabled = false;
                customSubcategoryInput.disabled = false;
                const options = subcategories['other'] || [];
                options.forEach(([value, label]) => {
                    console.log('Adding option - value:', value, 'label:', label);
                    const option = document.createElement('option');
                    option.value = value;
                    option.text = label;
                    subcategorySelect.appendChild(option);
                });
            } else if (category in subcategories) {
                subcategorySelect.disabled = false;
                customCategoryInput.disabled = true;
                customSubcategoryInput.disabled = true;
                const options = subcategories[category] || [];
                options.forEach(([value, label]) => {
                    console.log('Adding option - value:', value, 'label:', label);
                    const option = document.createElement('option');
                    option.value = value;
                    option.text = label;
                    subcategorySelect.appendChild(option);
                });
            } else {
                console.warn('Category not found in subcategories:', category);
            }

            // Restore the initial value if valid
            if (currentSubcategory && subcategories[category] && subcategories[category].some(([val]) => val === currentSubcategory)) {
                subcategorySelect.value = currentSubcategory;
                console.log('Restored subcategory to:', subcategorySelect.value);
            } else {
                console.log('Subcategory not restored, not in options:', currentSubcategory);
            }

            console.log('Final subcategory options:', Array.from(subcategorySelect.options).map(opt => ({ value: opt.value, text: opt.text })));
        }

        console.log('Initial category on load:', categorySelect.value);
        console.log('Initial subcategory from select:', subcategorySelect.value);
        categorySelect.addEventListener('change', updateSubcategories);
        updateSubcategories(); // Initial call
    } else {
        console.error('Category or subcategory select not found');
    }
});