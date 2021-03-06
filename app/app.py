from flask import Flask, render_template, request

from GreenButtonRest.clients import GreenButtonClient as gbc
from GreenButtonRest.parser import ParseXml

app = Flask(__name__)

app.config.update(dict(
    WTF_CSRF_ENABLED=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)


def fill_params(data, *exclude):
    params = {}
    for key, value in data.items():
        if key not in exclude and value != "":
            params[key] = value
    return params


@app.route("/", methods=['GET', 'POST'])
def main():
    data = {}
    for key, value in request.form.items():
        if value != "" or "_submit" in key:
            data[key] = value

    if "access_token" in request.form:
        token = data["access_token"]
        paths, params = [], {}
        if "app_info_submit" in request.form:
            endpoint = "/espi/1_1/resource/ApplicationInformation"
            params = fill_params(data, "access_token")
        elif "app_info_id_submit" in data:
            endpoint = "/espi/1_1/resource/ApplicationInformation"
            paths.append(data["app_info_id"])
        elif "auth_submit" in data:
            endpoint = "/espi/1_1/resource/Authorization"
            if "auth_id" in data:
                paths.append(data["auth_id"])
            params = fill_params(data, "access_token", "auth_id")
        elif "bulk_submit" in data:
            if "bulk_id" in data:
                endpoint = "/espi/1_1/resource/Batch/Bulk"
                paths.append(data["bulk_id"])
            elif "bulk_sub_id" in data:
                endpoint = "/espi/1_1/resource/Batch/Subscription"
                paths.append(data["bulk_sub_id"])
            elif "bulk_customer_id" in data:
                endpoint = "/espi/1_1/resource/Batch/RetailCustomer"
                paths.append(data["bulk_customer_id"])
            elif "bulk_sub_usage_id" in data:
                endpoint = "/espi/1_1/resource/Batch/Subscription/UsagePoint"
                paths.append(data["bulk_sub_id"])
            params = fill_params(data, "access_token", "bulk_radio", "bulk_id", "bulk_sub_id", "bulk_customer_id",
                                 "bulk_sub_usage_id")
        elif "epower_submit" in data:
            paths.append(data["epower_sub_id"])
            paths.append(data["epower_usagepoint_id"])
            if data["epower_radio"] == "quality":
                if data["epower_summary_id"] == "":
                    endpoint = "/espi/1_1/resource/Subscription/ElectricPowerQualitySummary"
                else:
                    endpoint = "/espi/1_1/resource/Subscription/ElectricPowerQualitySummarybyId"
                    paths.append(data["epower_summary_id"])
            else:
                if data["epower_summary"] == "":
                    endpoint = "/espi/1_1/resource/Subscription/ElectricPowerUsageSummary"
                else:
                    endpoint = "/espi/1_1/resource/Subscription/ElectricPowerUsageSummarybyId"
                    paths.append(data["epower_summary_id"])
            params = fill_params(data, "access_token", "epower_sub_id", "epower_usagepoint_id", "epower_summary_id",
                                 "epower_radio")
        elif "interval_submit" in data:
            if "interval_sub_id" in data:
                paths.append(data["interval_sub_id"])
                paths.append(data["interval_usagepoint_id"])
                paths.append(data["interval_meter_id"])
                if "interval_id" in data:
                    endpoint = "/espi/1_1/resource/Subscription/IntervalBlockbyId"
                    paths.append(data["interval_id"])
                else:
                    endpoint = "/espi/1_1/resource/Subscription/IntervalBlock"
            else:
                endpoint = "/espi/1_1/resource/IntervalBlock"
                if "interval_id" in data:
                    paths.append(data["interval_id"])
            params = fill_params(data, "access_token", "interval_sub_id", "interval_usage_id", "interval_meter_id",
                                 "interval_id")
        elif "local_time_submit" in data:
            endpoint = "/espi/1_1/resource/LocalTimeParameters"
            if "local_time_id" in data:
                paths.append(data["local_time_id"])
            params = fill_params(data, "access_token", "local_time_id")
        elif "meter_submit" in data:
            if "meter_sub_id" in data:
                paths.append(data["meter_sub_id"])
                paths.append(data["meter_usagepoint_id"])
                if "meter_id" in data:
                    endpoint = "/espi/1_1/resource/Subscription/MeterReadingbyId"
                    paths.append(data["meter_id"])
                else:
                    endpoint = "/espi/1_1/resource/Subscription/MeterReading"
            else:
                endpoint = "/espi/1_1/resource/MeterReading"
                if "meter_id" in data:
                    paths.append(data["meter_id"])
            params = fill_params(data, "access_token", "meter_sub_id", "meter_usagepoint_id", "meter_id")
        elif "reading_type_submit" in data:
            endpoint = "/espi/1_1/resource/ReadingType"
            if "reading_type_id" in data:
                paths.append(data["reading_type_id"])
            params = fill_params(data, "access_token", "reading_type_id")
        elif "server_status_submit" in data:
            endpoint = "/espi/1_1/resource/ReadServiceStatus"
        elif "usagepoint_submit" in data:
            if "usagepoint_sub_id" in data:
                if "usagepoint_id" in data:
                    endpoint = "/espi/1_1/resource/Subscription/UsagePointbyId"
                    paths.append(data["usagepoint_sub_id"])
                    paths.append(data["usagepoint_id"])
                else:
                    endpoint = "/espi/1_1/resource/Subscription/UsagePoint"
                    paths.append(data["usagepoint_sub_id"])
            else:
                endpoint = "/espi/1_1/resource/UsagePoint"
                if "usagepoint_id" in data:
                    paths.append(data["usagepoint_id"])
            params = fill_params(data, "access_token", "usagepoint_id", "usagepoint_sub_id")
        else:
            print("No endpoint defined!")
        try:
            call = gbc(token, endpoint, *paths, **params)
            response = call.execute()
            xml = ParseXml(response)
            # xml.parse()
            xml.tojson()
            error = "false"
        except:
            error = "true"
    try:
        return render_template("index.html", error=error, response=response)
    except:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
