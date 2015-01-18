import java.io.FileInputStream;
import java.lang.System;
import java.util.Properties;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyFile;
import org.python.core.PySystemState;
import org.python.util.JLineConsole;
import org.python.util.InteractiveConsole;
import org.python.util.InteractiveInterpreter;

public class Main {
    private static InteractiveConsole newInterpreter(boolean interactiveStdin) {
        if (!interactiveStdin) {
            return new InteractiveConsole();
        }

        String interpClass = PySystemState.registry.getProperty(
                "python.console", "");
        if (interpClass.length() > 0) {
            try {
                return (InteractiveConsole)Class.forName(
                        interpClass).newInstance();
            } catch (Throwable t) {
                // fall through
            }
        }
        return new JLineConsole();
    }

    public static void main(String[] args) throws PyException {
        PySystemState.initialize(
                PySystemState.getBaseProperties(),
                new Properties(), args);

        PySystemState systemState = Py.getSystemState();
        // Decide if stdin is interactive
        boolean interactive = ((PyFile)Py.defaultSystemState.stdin).isatty();
        if (!interactive) {
            systemState.ps1 = systemState.ps2 = Py.EmptyString;
        }

        // Now create an interpreter
        InteractiveConsole interp = newInterpreter(interactive);
        systemState.__setattr__("_jy_interpreter", Py.java2py(interp));
        interp.exec("try:\n MAINSTRMATCH\nexcept SystemExit: pass");
    }
}