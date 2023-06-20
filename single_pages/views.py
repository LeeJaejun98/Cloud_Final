from django.shortcuts import render
from blog.models import Post
import calendar
from datetime import datetime


class MyHtmlCalendar(calendar.HTMLCalendar):
    def myformatday(self, day, weekday, theyear, themonth):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            return '<td class="%s"><a href="/blog/search/%s/%s/%s">%d</a></td>' % \
                (self.cssclasses[weekday], themonth, theyear, day, day)

    def myformatweek(self, theweek, theyear, themonth):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.myformatday(d, wd, theyear, themonth) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.myformatweek(week, theyear, themonth))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)


def calendar_view(request):
    recent_posts = Post.objects.order_by('-create_at')[:5]
    year = datetime.now().year
    month = datetime.now().month
    next_month = month + 1
    next_year = year
    previous_month = month - 1
    previous_year = year
    if month == 12:
        next_month = 1
        next_year = year + 1
    elif month == 1:
        previous_month = 12
        previous_year = year - 1

    calendar_html = calc_calendar(year, month)
    return render(request, 'single_pages/main.html', {
        'calendar_html': calendar_html,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'year': year,
        'month': month,
        'recent_posts': recent_posts,
    })


def calendar_view_other(request, year, month):
    recent_posts = Post.objects.order_by('-create_at')[:5]
    next_month = month + 1
    next_year = year
    previous_month = month - 1
    previous_year = year
    if month == 12:
        next_month = 1
        next_year = year + 1
    elif month == 1:
        previous_month = 12
        previous_year = year - 1

    calendar_html = calc_calendar(year, month)
    return render(request, 'single_pages/main.html', {
        'calendar_html': calendar_html,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'year': year,
        'month': month,
        'recent_posts': recent_posts,
    })


def calc_calendar(year, month):
    cal = MyHtmlCalendar(calendar.SUNDAY)
    return cal.formatmonth(year, month)
