

def say(lang, phrase):
    dict = {
        'ru': {
            'rtw_changed': 'Статус изменился на Ready to Work (RTW)',
            'plan_short': 'Факт дольше плана (дни): ',
            'plan_long': 'Факт быстрее плана (дни)',
            'cant_skip': 'Невозможно изменить статус задачи, тк предыдущие задачи не закрыты'
            'preview_update': '---'
        },
        'en': {
            'rtw_changed': 'Status changed to Ready to Work (RTW)',
            'plan_short': 'Actual duration took longer than planned (days): ',
            'plan_long': 'Actual duration took faster than planned (days): ',            
            'cant_skip': 'Can\'t skip previous task(s). Status change aborted',
            'preview_update': 'Status automatically updated for task with new preview added'
        }
    }

    return dict[lang][phrase]