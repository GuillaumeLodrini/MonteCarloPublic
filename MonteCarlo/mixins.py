import csv
import io
import xlsxwriter

from django.http import HttpResponse
from django.utils.translation import gettext as _


# IMPORTANT NOTE: you have to install xlsxwriter package to use this mixin!
# > pip install XlsxWriter

class ExportCsvXlsxMixin:
    """
    Returns a FILE HTTP response object, with a CSV XLSX extract of all the selected objects.
    """

    def get_actions(self, request):
        """
        Add the different actions to the list of actions.
        """

        # Export as CSV
        if 'export_as_csv' not in self.actions:
            self.actions.append('export_as_csv')

        # Export as XLSX
        if 'export_as_xlsx' not in self.actions:
            self.actions.append('export_as_xlsx')

        return super().get_actions(request)

    def export_as_csv(self, request, queryset):
        # Get all field names
        meta = self.model._meta
        verbose_field_names = [field.verbose_name for field in meta.fields]
        field_names = [field.name for field in meta.fields]

        # Create the response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'

        # Write the first row with all field names
        writer = csv.writer(response)
        writer.writerow(verbose_field_names)

        # Export each instance selected in a new row
        for obj in queryset:
            values = []

            for field in field_names:
                value = getattr(obj, field)
                values += [str(value) if value is not None else '']

            writer.writerow(values)

        return response

    # Add a description for the action
    export_as_csv.short_description = _('Exporter au format CSV')

    def export_as_xlsx(self, request, queryset):
        # Create the XLXS file and attribute it some space in the short term memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Make the columns title and name and write them in the file
        row_num = 0
        bold = workbook.add_format({'bold': True})

        # Get all field names
        meta = self.model._meta
        verbose_field_names = [field.verbose_name for field in meta.fields]
        field_names = [field.name for field in meta.fields]

        # Write the first row with all field names
        for col_num in range(len(verbose_field_names)):
            worksheet.write(row_num, col_num, str(verbose_field_names[col_num]), bold)

        # Export each instance selected in a new row
        for obj in queryset:
            rows = []

            for field in field_names:
                value = getattr(obj, field)
                rows += [str(value) if value is not None else '']

            row_num += 1

            for col_num in range(len(field_names)):
                worksheet.write(row_num, col_num, rows[col_num])

        # Save the stylesheet and complete the files meta datas then send it to the user.
        workbook.close()
        output.seek(0)

        # Create the response object
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'

        return response

    # Add a description for the action
    export_as_xlsx.short_description = _('Exporter au format XLSX')
