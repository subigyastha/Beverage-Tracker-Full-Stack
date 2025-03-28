// document.addEventListener('DOMContentLoaded', function() {
//     const categorySelect = document.getElementById('id_category');
//     const subcategorySelect = document.getElementById('id_subcategory');
//     const subcategories = {{ subcategories_json|safe }};

//     function updateSubcategories() {
//         const category = categorySelect.value;
//         subcategorySelect.innerHTML = '<option value="">---------</option>';
        
//         if (category && subcategories[category]) {
//             subcategories[category].forEach(function(subcategory) {
//                 const option = document.createElement('option');
//                 option.value = subcategory[0];
//                 option.textContent = subcategory[1];
//                 subcategorySelect.appendChild(option);
//             });
//         }
//     }

//     categorySelect.addEventListener('change', updateSubcategories);
    
//     // Initialize on page load if category is already selected
//     if (categorySelect.value) {
//         updateSubcategories();
//     }
// });
