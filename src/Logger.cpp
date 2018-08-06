/// FicTrac http://rjdmoore.net/fictrac/
/// \file       Logger.cpp
/// \brief      Simple thread-safe logger.
/// \author     Richard Moore
/// \copyright  CC BY-NC-SA 3.0

#include "Logger.h"

#include "Timing.h"

#include <cstdio>   // vsnprintf
#include <cstdarg>  // va_list, va_start, va_end
#include <iostream> // cout

using namespace std;

static string _fn = "fictrac.log";
void Logger::setLogFile(std::string fn)
{
    _fn = fn;
}

Logger::Logger()
{
    // create log writer
    _log = unique_ptr<Recorder>(new Recorder(_fn));
}

Logger::~Logger()
{
}

void Logger::setVerbosity(std::string v) {
    if ((v.compare("DBG") == 0) || (v.compare("dbg") == 0)) {
        setVerbosity(DBG);
    }
    else if ((v.compare("INF") == 0) || (v.compare("inf") == 0)) {
        setVerbosity(INF);
    }
    else if ((v.compare("WRN") == 0) || (v.compare("wrn") == 0)) {
        setVerbosity(WRN);
    }
    else if ((v.compare("ERR") == 0) || (v.compare("err") == 0)) {
        setVerbosity(ERR);
    }
    else {
        setVerbosity(INF);
        LOG_WRN("Warning, verbosity (%s) not recognised! Defaulting to INFO.", v.c_str());
    }
}

/// Thread-safe printf wrapper.
void Logger::mprintf(LogLevel lvl, string func, string format, ...)
{
    static Logger log;   // *the* logger instance

    static const int buf_size = 1024;
    static char buf[buf_size];

    // not re-entrant
    lock_guard<mutex> l1(log._pMutex);

    // logging format
    if (lvl != PRT) {
        format = to_string(elapsed_secs()) + "::" + func + ": " + format + "\n";
    } else {
        format = format + "\n";
    }

    // expand args
    if ((int)lvl >= (int)verbosity()) {
        va_list args;
        va_start(args, format);
        vsnprintf(buf, buf_size, format.c_str(), args);
        va_end(args);

        // print to console
        cout << buf;

        // don't log display text to file
        if (lvl != PRT) {
            // async logging to file
            log._log->addMsg(string(buf));
        }
    }
}