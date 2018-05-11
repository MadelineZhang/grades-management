# this application keeps track of my grades
# hover over data point to see grade and GPA

import yaml
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FuncTickFormatter, HoverTool
from bokeh.io import show


class Data:
    def __init__(self, syllabus_file):
        self.syllabus_file = syllabus_file
        self.data = self.load_yml()
        self.course_list = [course for course in self.data]
        self.current_grade_list= self.calc_total()
        self.GPA_list = [GPA_generator(grade) for grade in self.current_grade_list]
        self.dict = {'courses': self.course_list,
                     'grade': self.current_grade_list,
                     'index': [0, 1, 2, 3, 4, 5],
                     'GPA': self.GPA_list}

        self.source = ColumnDataSource(self.dict)
        print(self.source.data)

    def load_yml(self):
        with open(self.syllabus_file, 'r') as yml_file:
            info = yaml.load(yml_file)
        return info

    def calc_total(self):
        grade_list = [0, 0, 0, 0, 0, 0]
        for i,course in enumerate(self.data):
            for type in self.data[course]:
                print(self.data[course][type])
                if self.data[course][type]['grade'] <0.01 :
                    grade_list[i] += self.data[course][type]['percent'] * 100
                else:
                    grade_list[i] += self.data[course][type]['percent'] * self.data[course][type]['grade']
        print(grade_list)
        return grade_list


def plot(source):
    p = figure(x_axis_label='courses', y_axis_label='grade', y_range=(50, 105),
               plot_width=600, plot_height=600, title='grade monitor')
    p.circle('index', 'grade', size=10, alpha=0.9, source=source)

    label_dict = {}

    for i, s in enumerate(source.data['courses']):
        label_dict[i] = s

    p.xaxis.formatter = FuncTickFormatter(code="""
            var labels = %s;
            return labels[tick];
        """ %label_dict)

    hover = HoverTool(tooltips=[('grade', '@grade'), ('GPA','@GPA')])
    p.add_tools(hover)

    return p


def GPA_generator(grade):
    grade = round(float(grade))
    if grade >= 85:
        GPA = 4.0
    elif 80 <= grade <= 84:
        GPA = 3.7
    elif 77 <= grade <= 79:
        GPA = 3.3
    elif 73 <= grade <= 76:
        GPA = 3.0
    elif 70 <= grade <= 72:
        GPA = 2.7
    elif 67 <= grade <= 69:
        GPA = 2.3
    elif 63 <= grade <= 66:
        GPA = 2.0
    elif 60 <= grade <= 62:
        GPA = 1.7
    else:
        print('Failed')
        GPA = 0
    return GPA


def main(grade_file):
    data = Data(grade_file)
    source = data.source
    print('source'+ str(source.data))
    p = plot(source)
    show(p)

main('second_winter.yml')
