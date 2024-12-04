function send_url_to_modal_cart(itemId) {
        var url = "remove/item_id/".replace('item_id', itemId);
        document.getElementById('remove-link').setAttribute('href', url);
    }

function send_url_to_modal_shop(itemId) {
        var url = "delete_product/item_id/".replace('item_id', itemId);
        document.getElementById('remove-link').setAttribute('action', url);
    }

function send_url_to_modal_category(itemId) {
        var url = "delete_category/item_id/".replace('item_id', itemId);
        document.getElementById('remove-link').setAttribute('action', url);
    }

function send_url_to_modal_subcategory(itemId) {
        var url = "delete_subcategory/item_id/".replace('item_id', itemId);
        document.getElementById('remove-link').setAttribute('action', url);
    }