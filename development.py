manager.spawn_instance()
manager.delete_latest()

for i in range(19):
    manager.spawn_instance()

for i in range(len(manager.browser_instances)):
    manager.delete_latest()

for instance in manager.browser_instances:
    instance.driver.set_window_size(640, 480)
    instance.driver.find_element_by_css_selector('button[data-a-target="player-settings-button"]').click()
    instance.driver.find_element_by_css_selector('button[data-a-target="player-settings-menu-item-quality"]').click()
    instance.driver.find_elements_by_css_selector('div[data-a-target="player-settings-submenu-quality-option"]')[-1].click()
    instance.driver.set_window_size(500, 300)

for instance in manager.browser_instances:
    instance.driver.set_window_size(640, 480)
    instance.driver.refresh()
    instance.modify_driver()

for instance in manager.browser_instances:
    instance.driver.set_window_size(640, 480)
    instance.modify_driver()
