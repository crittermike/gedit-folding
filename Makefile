GEDIT_PLUGIN_DIR = ~/.local/share/gedit/plugins

install:
	@if [ ! -d $(GEDIT_PLUGIN_DIR) ]; then \
		mkdir -p $(GEDIT_PLUGIN_DIR);\
	fi
	@echo "installing folding plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/folding*;
	@cp -R folding* $(GEDIT_PLUGIN_DIR);

uninstall:
	@echo "uninstalling folding plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/folding*;
