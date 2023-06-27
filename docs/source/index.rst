utdf2gmns
====================================
| **Authors**: Xiangyong Luo, Xuesong (Simon) Zhou
| **Email**: luoxiangyong01@gmail.com, xzhou74@asu.edu


utdf2gmns is a tool to convert utdf file to GMNS format:  **synchro utdf format to gmns signal timing format at movement layer**

**If you use utdf2gmns in your research, please cite: https://github.com/xyluo25/utdf2gmns **

Required Data Input Files:
--------------------------


* [X] UTDF.csv
* [X] node.csv (GMNS format)
* [X] movement.csv (GMNS format)

**Produced outputs**
------------------------

**If input folder have UTDF.csv only, outputs are:**

* A dictionary store utdf data with keys: Networks, Node, Links, Timeplans, Lanes, and utdf_intersection
* A file named utdf2gmns.pickle to store dictionary object.

**If input folder have extra node.csv and movement.csv, outputs are:**

* Two files named:  movement_utdf.csv and utdf_intersection.csv

Sample results: `datasets <https://github.com/asu-trans-ai-lab/utdf2gmns/tree/main/datasets>`_


**Package dependencies**
------------------------

* [X] geocoder==1.38.1
* [X] pandas==1.4.4

**Data Conversion Steps**
-------------------------

Step 1: Read UTDF.csv file and perform geocoding, then produce utdf_geo, utdf_lane, and utdf_phase_timeplans.

Step 2: Match four files (utdf_geo, node, utdf_lane, utdf_pahse_timeplans, movement) to produce movement_utdf


**Call for Contributions**
--------------------------

The utdf2gmns project welcomes your expertise and enthusiasm!

Small improvements or fixes are always appreciated. If you are considering larger contributions to the source code, please contact us through email:

    Xiangyong Luo :  luoxiangyong01@gmail.com

    Dr. Xuesong Simon Zhou :  xzhou74@asu.edu

Writing code isn't the only way to contribute to utdf2gmns. You can also:

* review pull requests
* help us stay on top of new and old issues
* develop tutorials, presentations, and other educational materials
* develop graphic design for our brand assets and promotional materials
* translate website content
* help with outreach and onboard new contributors
* write grant proposals and help with other fundraising efforts

For more information about the ways you can contribute to utdf2gmns, visit [our GitHub](https://github.com/asu-trans-ai-lab/utdf2gmns). If you' re unsure where to start or how your skills fit in, reach out! You can ask by opening a new issue or leaving a comment on a relevant issue that is already open on GitHub.

Contents
====================================

.. toctree::
   :maxdepth: 2

   installation
   gmns
   quick-start
   todo-list
   functions
   api
   acknowledgement


For program source code and sample network files, readers can visit the project  `homepage`_
at ASU Trans+AI Lab Github.


.. _`GMNS`: https://github.com/zephyr-data-specs/GMNS
.. _`homepage`: https://github.com/asu-trans-ai-lab
