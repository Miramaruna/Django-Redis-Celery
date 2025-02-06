
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Подтверждение удаления задачи
            document.querySelectorAll('.delete-btn').forEach(function(button) {
                button.addEventListener('click', function(event) {
                    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
                        event.preventDefault();
                    }
                });
            });

            // Редактирование задачи по двойному клику
            document.querySelectorAll('.todo-title').forEach(function(span) {
                span.addEventListener('dblclick', function() {
                    const currentText = span.innerText;
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = currentText;
                    span.replaceWith(input);
                    input.focus();

                    input.addEventListener('blur', function() {
                        span.innerText = input.value;
                        input.replaceWith(span);
                        // Здесь можно отправить AJAX-запрос для обновления задачи на сервере
                    });
                });
            });
        });
    </script>