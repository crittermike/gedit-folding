# -*- coding: utf-8 -*-
import gtk
import gedit
import traceback


ui_str = """<ui>
    <menubar name="MenuBar">
        <menu name="ToolsMenu" action="Tools">
            <placeholder name="ToolsOps_2">
                <menuitem name="Folding" action="FoldingPyFold"/>
                <menuitem name="FoldingAll" action="FoldingPyFoldAll"/>
                <menuitem name="FoldingUnf" action="FoldingPyUnFold"/>
            </placeholder>
        </menu>
    </menubar>
</ui>
"""

DEBUG = True

def hide_exception(f):
    """Allows hiding exceptions for above code."""
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BaseException as bexc:
            print traceback.format_exc()
    return wrapper
            

class FoldingPyWindowHelper():
    
    DEFAULT_LEVEL_EMPTY_LINE = 1000
    
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        self._insert_menu()
        self.update_ui()

    def deactivate(self):
        self._remove_menu()
        self._window = None
        self._plugin = None
        self._action_group = None

    def _insert_menu(self):
        manager = self._window.get_ui_manager()
        self._action_group = gtk.ActionGroup("FoldingPyPluginActions")
        self._action_group.add_actions(
            [
                (
                    "FoldingPyFold", None, "Fold Toggle",
                    "<Alt>Z", "Fold Toggle",
                    self.fold
                ),
                (
                    "FoldingPyFoldAll", None, "Fold All",
                    "<Alt>Q", "Fold All",
                    self.__fold_all
                ),
                (
                    "FoldingPyUnFold", None, "Unfold All",
                    "<Alt>X", "Unfold All",
                    self.__unfold_all
                ),
            ],
        )
        manager.insert_action_group(self._action_group, -1)
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        manager = self._window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()

    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)
        self.doc=self._window.get_active_document()
        if self.doc:
            self.view=self._window.get_active_view()
            #self.view.connect('key-press-event', self.fold_off)
            
            table=self.doc.get_tag_table()
            self.fld=table.lookup('fld')
            if self.fld==None:
                self.fld=self.doc.create_tag('fld',foreground="#333333",paragraph_background="#aadc5c")
            self.inv=table.lookup('inv')
            if self.inv==None:
                self.inv=self.doc.create_tag('inv',invisible=True)

    def detect_sps(self,sps):
        """Detect and return spaces at beginning of line."""
        sps_lstrip=sps.lstrip()
        if not len(sps_lstrip):
            return self.DEFAULT_LEVEL_EMPTY_LINE # empty line
        i=sps.index(sps_lstrip)
        sps=sps[:i]
        return sps.count(' ')+sps.count('\t')*self.view.get_tab_width()

    def __unfold_all(self, action=None):
        """Unfold all document."""
        s,e=self.doc.get_bounds()
        self.doc.remove_tag(self.fld,s,e)
        self.doc.remove_tag(self.inv,s,e)
        print "SimpleFolding plugin: remove all fold"
    
    def __fold_all(self, action=None):
        """Fold all possible text."""
        self.__unfold_all()
        s,e=self.doc.get_bounds()
        while e.backward_line():
            self.__fold(e)
        print "SimpleFolding plugin: fold all"
        

    def fold_off(self,widget,e=None):
        """Method that has been used with self.view.connect('key-press-event', self.fold_off)."""
        # e.hardware_keycode contains the current key, and self.keycode contains the previous key (modifier probably)
        if e.hardware_keycode==53 and self.keycode==64: # X + Alt
            self.__unfold_all()
            self.keycode=53
        if e.hardware_keycode==19 and self.keycode==64: # 0 + Alt (but real shortcut is Alt+Q now)
            self.__fold_all()
            self.keycode=19
        else:
            self.keycode=e.hardware_keycode

    @hide_exception
    def __unfold(self, a):
        """Unfold a piece of text. a is the line highlighted in green."""
        # go to beginning of line
        a.set_line_offset(0)
        b=a.copy()
        # b goes to the end of the first line
        b.forward_line()
        self.doc.remove_tag(self.fld,a,b)
        # first line
        firstline = a.get_text(b)
        firstlinenb = a.get_line()
        baselevel = self.detect_sps(firstline)
        # c beginning of current line
        c = a.copy()
        c.forward_line()
        # d end of current line
        d = b.copy()
        d.forward_line()
        # text of current line
        textline = c.get_text(d)
        curlinenb = c.get_line()
        level = self.detect_sps(textline)
        pause_unfold_while_level_gt = None
        while level > baselevel:
            if pause_unfold_while_level_gt is not None and level <= pause_unfold_while_level_gt:
                pause_unfold_while_level_gt = None
            if pause_unfold_while_level_gt is None:
                    self.doc.remove_tag(self.inv,c,d)
            if c.has_tag(self.fld) and pause_unfold_while_level_gt is None:
                    pause_unfold_while_level_gt = level
            if not d.forward_line():
                break
            c.forward_line()
            textline = c.get_text(d)
            curlinenb = c.get_line()
            level = self.detect_sps(textline)
        
        print "SimpleFolding CMR plugin: remove one fold"

    @hide_exception
    def __fold(self, a):
        """Fold a piece of text. a is the line that will be highlighted in green."""
        # go to beginning of line
        a.set_line_offset(0)
        b=a.copy()
        # b goes to the end of the first line
        b.forward_line()
        # first line
        firstline = a.get_text(b)
        firstlinenb = a.get_line()
        baselevel = self.detect_sps(firstline)
        #if DEBUG: print "Level:", baselevel, "Line:",firstlinenb,  "Text:", repr(firstline)
        # c beginning of current line
        # d end of current line
        d = b.copy()
        d.forward_line()
        c = a.copy()
        c.forward_line()
        # text of current line
        textline = c.get_text(d)
        curlinenb = c.get_line()
        level = self.detect_sps(textline)
        first = True
        first_empty_lines = None
        #if DEBUG: print "\tLevel:", level, "Line:",curlinenb,  "Text:", repr(textline)
        while level > baselevel:
            # special case if first lines are empty
            if level == self.DEFAULT_LEVEL_EMPTY_LINE and first:
                if first_empty_lines is None:
                    first_empty_lines = [c.copy(), d.copy()]
                else:
                    first_empty_lines[1] = d.copy()
            else: # not an empty line (or after first folded line)
                self.doc.apply_tag(self.inv,c,d)
                if first:
                    self.doc.apply_tag(self.fld,a,b)
                    first = False
                    if first_empty_lines is not None:
                        self.doc.apply_tag(self.inv,*first_empty_lines)
            if not d.forward_line():
                break
            c.forward_line()
            textline = c.get_text(d)
            curlinenb = c.get_line()
            level = self.detect_sps(textline)
            #if DEBUG: print "\tLevel:", level, "Line:",curlinenb,  "Text:", repr(textline)
        
        print "SimpleFolding CMR plugin:", "add one fold " if not first else "unable to add one fold",  "on line %s" % firstlinenb

    def __fold_selection(self, action=None):
        """Fold a selection."""
        a,c=self.doc.get_selection_bounds()
        b=a.copy()
        a.set_line_offset(0)
        b.forward_line()
        c.forward_line()
        self.doc.apply_tag(self.fld,a,b)
        #self.doc.remove_tag(self.fld,b,c)
        #self.doc.remove_tag(self.inv,b,c)
        self.doc.apply_tag(self.inv,b,c)
        print "SimpleFolding plugin: create fold by selection"

    def fold(self, action):
        """Method that toggles the fold."""
        a=self.doc.get_iter_at_mark(self.doc.get_insert())
        if a.has_tag(self.fld):
            self.__unfold(a)
        elif len(self.doc.get_selection_bounds())==2:
            self.__fold_selection()
        else:
            self.__fold(a)
            


    def fold_old(self, action):
        """Old method used to fold."""
        a=self.doc.get_iter_at_mark(self.doc.get_insert())
        if a.has_tag(self.fld):
            try:
                a.set_line_offset(0)
                b=a.copy()
                b.forward_line()
                self.doc.remove_tag(self.fld,a,b)
                a.forward_to_tag_toggle(self.inv)
                b.forward_to_tag_toggle(self.inv)
                self.doc.remove_tag(self.inv,a,b)
                print "SimpleFolding plugin: remove one fold"
            except:
                pass

        elif len(self.doc.get_selection_bounds())==2:
            a,c=self.doc.get_selection_bounds()
            b=a.copy()
            a.set_line_offset(0)
            b.forward_line()
            c.forward_line()
            self.doc.apply_tag(self.fld,a,b)
            self.doc.remove_tag(self.fld,b,c)
            self.doc.remove_tag(self.inv,b,c)
            self.doc.apply_tag(self.inv,b,c)
            print "SimpleFolding plugin: create fold by selection"

        else:
            s=a.copy()
            s.set_line_offset(0)
            # number of line
            line = s.get_line()
            e=s.copy()
            e.forward_line()
            t=s.get_text(e)
            if t.strip()!="":
                main_indent = self.detect_sps(s.get_text(e))
                ns=s.copy()
                fin=ns.copy()
                while 1==1:
                    if ns.forward_line():
                        ne=ns.copy()
                        if ne.get_char()=="\n":
                            continue
                        ne.forward_to_line_end()
                        text=ns.get_text(ne)
                        if text.strip()=="":
                            continue
                        child_indent=self.detect_sps(text)
                        if child_indent <= main_indent:
                            break
                        else:
                            line=ns.get_line()
                        fin=ns.copy()
                        fin.set_line(line)
                        fin.forward_line()
                    else:
                        fin=ne.copy()
                        fin.forward_to_end()
                        line=fin.get_line()
                        break
                
                if s.get_line()<line:
                    self.doc.apply_tag(self.fld,s,e)
                    self.doc.remove_tag(self.fld,e,fin)
                    self.doc.remove_tag(self.inv,e,fin)
                    self.doc.apply_tag(self.inv,e,fin)
                    print "SimpleFolding plugin: create fold by indent"


class FoldingPyPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}
    def activate(self, window):
        #print "gedit file: ", gedit.__file__
        self._instances[window] = FoldingPyWindowHelper(self, window)
    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]
    def update_ui(self, window):
        self._instances[window].update_ui()
